import os
import re
import sys

import django
from django.db.models.fields.related import ForeignKey, ManyToOneRel, ManyToManyRel
from django.db.models.fields import IntegerField, CharField, FloatField, TextField, DecimalField, DateField, \
    DateTimeField, BooleanField, TimeField
from django.db.models.fields.json import JSONField

# Add the parent directory to sys.path so Python can find your modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
print(f"Project root: {project_root}")

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zbackend.settings")
django.setup()

# Print paths for debugging
print("################# script_dir", os.path.dirname(__file__))
print("################# sys.path", sys.path)
print("################# Available modules:", [m for m in sys.modules.keys() if not m.startswith('_') and '.' not in m])

# Constants
exceptions_insert_fields = ['is_active', 'is_deleted', 'created_at', 'updated_at', 'deleted_at']
exceptions_update_fields = ['created_at', 'updated_at', 'deleted_at', 'created_date', 'updated_date']
folder_name = 'agraphql'

# Get the directory of the current script
script_dir = os.path.dirname(__file__)


def nomenclature(model_name):
    return '_'.join(re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])', model_name)).lower()


# Try to list all models using Django's app registry
try:
    from django.apps import apps

    # Get all models from the api app
    tables = []
    for model in apps.get_models():
        model_module = model.__module__
        print(f"Found model: {model.__name__} in module {model_module}")
        if model_module.startswith('api.'):
            tables.append((model.__name__, model))

    print(f"Found {len(tables)} models from api app")

    if not tables:
        # If no models found, try to get all models
        tables = [(model.__name__, model) for model in apps.get_models()]
        print(f"Found {len(tables)} models from all apps")
except Exception as e:
    print(f"Error getting models: {e}")
    tables = []


# Function to create directories and files
def create_directories_and_files(model_name):
    # Create base directory if it doesn't exist
    base_dir = os.path.join(script_dir, folder_name)
    model_dir = os.path.join(base_dir, nomenclature(model_name))

    # Create all directories
    os.makedirs(model_dir, exist_ok=True)
    print(f"Created directory: {model_dir}")

    return model_dir


def generate_types(model_name, model_class):
    # Get the directory path
    model_dir = create_directories_and_files(model_name)

    # Create the types.py file in the model directory
    file_path = os.path.join(model_dir, 'types.py')
    print(f"Creating file: {file_path}")

    with open(file_path, 'w') as types_file:
        types_file.write(f"""from query_optimizer import DjangoObjectType, filter
from api import models
import django_filters
import graphene


class {model_name}Filter(django_filters.FilterSet):
    order_by = django_filters.OrderingFilter(
        fields=(
            [
                field.name + "__id" if field.is_relation else field.name
                for field in models.{model_name}._meta.fields
            ]
        )
    )
    id__exclude_in = django_filters.ModelMultipleChoiceFilter(
        queryset=models.{model_name}.objects,
        method='filter_id_exclude',
    )

    def filter_id_exclude(self, queryset, name, value):
        if value:
            exclude_ids = [obj.id for obj in value]
            return queryset.exclude(id__in=exclude_ids)
        return queryset

    class Meta:
        model = models.{model_name}
        fields = {{field.name + "__id" if field.is_relation else field.name: ["exact", "in"] for field in
                  models.{model_name}._meta.fields}}
""")
        exclude = [field.name for field in model_class._meta.get_fields() if isinstance(field, JSONField)]
        if exclude:
            types_file.write(f"        exclude = {exclude}\n")
        types_file.write(f"""
class {model_name}Type(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)

    class Meta:
        model = models.{model_name}
        filterset_class = {model_name}Filter
        interfaces = (graphene.relay.Node,)
""")


def generate_mutations(model_name, model_class):
    model_dir = create_directories_and_files(model_name)
    file_path = os.path.join(model_dir, 'mutations.py')
    print(f"Creating file: {file_path}")

    # Get only the model's direct fields (no reverse relations)
    fields = model_class._meta.fields
    model_var_name = nomenclature(model_name)

    mutations_content = f'''import graphene
from django.core.exceptions import ValidationError
from api import models
from .types import {model_name}Type
from django.db import transaction


def get_instance_from_global_id(model, global_id, field_name):
    """Helper to get instance from global ID with proper error handling."""
    try:
        return model.objects.get(pk=global_id)
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid ID format for {{field_name}}")
    except model.DoesNotExist:
        raise ValidationError(f"{{model.__name__}} instance not found for {{field_name}}")
'''

    with open(file_path, 'w') as mutations_file:
        mutations_file.write(mutations_content)

        # Create Mutation
        mutations_file.write(f"""

class Create{model_name}(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    {model_var_name} = graphene.Field({model_name}Type)

    class Arguments:
""")

        # Generate Arguments for Create - only direct fields
        for field in fields:
            if field.name in exceptions_insert_fields:
                continue

            field_type = get_graphene_field_type(field)

            # Déterminer si le champ est requis
            if field.is_relation:
                required = True  # Les relations sont toujours requises
            else:
                required = (not field.null and not field.has_default() and field.name != 'id')

            # Gestion des cas particuliers
            if field.name in ['updated_by', 'added_by']:
                required_str = "required=True"
            elif field.name == "metas":
                required_str = "default_value=None"
            else:
                required_str = "required=True" if required else ""

            mutations_file.write(f"        {field.name} = {field_type}({required_str})\n")

        # Create mutate method
        mutations_file.write(f"""
    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, **kwargs):
        try:
            # Convert foreign keys to instances
            create_kwargs = {{}}
            for field in models.{model_name}._meta.fields:  # Using fields only
                if field.name in kwargs and kwargs[field.name] is not None:
                    if field.is_relation:
                        related_model = field.related_model
                        create_kwargs[field.name] = get_instance_from_global_id(
                            related_model, 
                            kwargs[field.name],
                            field.name
                        )
                    else:
                        create_kwargs[field.name] = kwargs[field.name]
            create_kwargs["added_by"] = models.{model_name}.objects.get(pk=kwargs['added_by'])
            instance = models.{model_name}.objects.create(**create_kwargs)
            return Create{model_name}(
                success=True,
                message="{model_name} created successfully",
                {model_var_name}=instance
            )
        except ValidationError as e:
            return Create{model_name}(success=False, message=e.message)
        except Exception as e:
            return Create{model_name}(
                success=False, 
                message=f"Error creating {model_name}: {{str(e)}}"
            )
""")

        # Update Mutation
        mutations_file.write(f"""

class Update{model_name}(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    {model_var_name} = graphene.Field({model_name}Type)

    class Arguments:
        id = graphene.ID(required=True)
""")

        # Generate Arguments for Update - only direct fields
        for field in fields:
            if field.name in exceptions_update_fields or field.name == 'id':
                continue

            field_type = get_graphene_field_type(field)
            mutations_file.write(f"        {field.name} = {field_type}()\n")

        # Update mutate method
        mutations_file.write(f"""
    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, id, **kwargs):
        try:
            # Get instance
            instance = models.{model_name}.objects.get(pk=id)

            # Update fields - only direct fields
            for field in models.{model_name}._meta.fields:
                if field.name in kwargs and kwargs[field.name] is not None:
                    if field.is_relation:
                        related_model = field.related_model
                        setattr(
                            instance, 
                            field.name, 
                            get_instance_from_global_id(
                                related_model,
                                kwargs[field.name],
                                field.name
                            )
                        )
                    else:
                        setattr(instance, field.name, kwargs[field.name])
            instance.updated_by = models.{model_name}.objects.get(pk=kwargs['updated_by'])
            instance.full_clean()
            instance.save()
            return Update{model_name}(
                success=True,
                message="{model_name} updated successfully",
                {model_var_name}=instance
            )
        except models.{model_name}.DoesNotExist:
            return Update{model_name}(
                success=False,
                message="{model_name} not found"
            )
        except ValidationError as e:
            return Update{model_name}(success=False, message=e.message)
        except Exception as e:
            return Update{model_name}(
                success=False, 
                message=f"Error updating {model_name}: {{str(e)}}"
            )
""")

        # Delete Mutation
        mutations_file.write(f"""

class Delete{model_name}(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, id):
        try:
            instance = models.{model_name}.objects.get(pk=id)
            instance.is_deleted=True
            instance._is_active=False
            instance.save()
            return Delete{model_name}(
                success=True,
                message="{model_name} deleted successfully"
            )
        except models.{model_name}.DoesNotExist:
            return Delete{model_name}(
                success=False,
                message="{model_name} not found"
            )
        except Exception as e:
            return Delete{model_name}(
                success=False,
                message=f"Error deleting {model_name}: {{str(e)}}"
            )

""")


def get_graphene_field_type(field):
    """Helper function to map Django field types to Graphene types."""
    if isinstance(field, (CharField, TextField)):
        return "graphene.String"
    elif isinstance(field, IntegerField):
        return "graphene.Int"
    elif isinstance(field, BooleanField):
        return "graphene.Boolean"
    elif isinstance(field, DateTimeField):
        return "graphene.DateTime"
    elif isinstance(field, DateField):
        return "graphene.Date"
    elif isinstance(field, FloatField):
        return "graphene.Float"
    elif isinstance(field, DecimalField):
        return "graphene.Decimal"
    elif isinstance(field, TimeField):
        return "graphene.Time"
    elif isinstance(field, JSONField):
        return "graphene.JSONString"
    elif field.is_relation:
        return "graphene.ID"
    return "graphene.String"


def generate_queries(model_name):
    model_dir = create_directories_and_files(model_name)
    file_path = os.path.join(model_dir, 'queries.py')
    print(f"Creating file: {file_path}")

    with open(file_path, 'w') as queries_file:
        queries_file.write(f"""import graphene
from query_optimizer import DjangoConnectionField
from .types import {model_name}Type

class {model_name}Query(graphene.ObjectType):
    {nomenclature(model_name)} = DjangoConnectionField({model_name}Type)
""")


def generate_meta(model_name, model_class):
    model_dir = create_directories_and_files(model_name)
    file_path = os.path.join(model_dir, f'{nomenclature(model_name)}_meta.py')
    print(f"Creating file: {file_path}")

    with open(file_path, 'w') as meta_file:
        meta_file.write(f"""create_{nomenclature(model_name)} = \"\"\"
# Mutation `create{model_name}`

This mutation creates a new {model_name} in the system.

## **Parameters:
""")
        for field in model_class._meta.get_fields():
            if field.name not in exceptions_insert_fields:
                if isinstance(field, ForeignKey):
                    meta_file.write(f"- `{field.name}` (ID!) : Related {field.related_model.__name__} ID\n")
                elif isinstance(field, JSONField):
                    meta_file.write(f"- `{field.name}` (JSONString) : JSON data for {field.name}\n")
                elif isinstance(field, (CharField, TextField)):
                    meta_file.write(f"- `{field.name}` (String) : {field.name.replace('_', ' ').title()}\n")
                elif isinstance(field, IntegerField):
                    meta_file.write(f"- `{field.name}` (Int) : {field.name.replace('_', ' ').title()}\n")
                elif isinstance(field, FloatField):
                    meta_file.write(f"- `{field.name}` (Float) : {field.name.replace('_', ' ').title()}\n")
                elif isinstance(field, BooleanField):
                    meta_file.write(f"- `{field.name}` (Boolean) : {field.name.replace('_', ' ').title()}\n")
                elif isinstance(field, DateField):
                    meta_file.write(f"- `{field.name}` (Date) : {field.name.replace('_', ' ').title()}\n")
                elif isinstance(field, DateTimeField):
                    meta_file.write(f"- `{field.name}` (DateTime) : {field.name.replace('_', ' ').title()}\n")

        meta_file.write(f"""
## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `{nomenclature(model_name)}` ({model_name}Type) : Created {model_name} object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation Create{model_name}(
""")
        for field in model_class._meta.get_fields():
            if field.name not in exceptions_insert_fields:
                if isinstance(field, ForeignKey):
                    meta_file.write(f"    ${field.name}: ID!\n")
                elif isinstance(field, JSONField):
                    meta_file.write(f"    ${field.name}: JSONString\n")
                elif isinstance(field, (CharField, TextField)):
                    meta_file.write(f"    ${field.name}: String\n")
                elif isinstance(field, IntegerField):
                    meta_file.write(f"    ${field.name}: Int\n")
                elif isinstance(field, FloatField):
                    meta_file.write(f"    ${field.name}: Float\n")
                elif isinstance(field, BooleanField):
                    meta_file.write(f"    ${field.name}: Boolean\n")
                elif isinstance(field, DateField):
                    meta_file.write(f"    ${field.name}: Date\n")
                elif isinstance(field, DateTimeField):
                    meta_file.write(f"    ${field.name}: DateTime\n")

        meta_file.write(f""") {{
    create{model_name}(
""")
        meta_file.write(f"""    ) {{
        success
        message
        {nomenclature(model_name)} {{
            id
""")
        for field in model_class._meta.get_fields():
            if not isinstance(field, (ManyToOneRel, ManyToManyRel)):
                field_name = field.name
                if field_name not in ['id']:
                    meta_file.write(f"            {field_name}\n")

        meta_file.write(f"""        }}
        errors
    }}
}}
```\"\"\"

update_{nomenclature(model_name)} = \"\"\"
# Mutation `update{model_name}`

This mutation updates an existing {model_name}.

## **Parameters:
- `id` (ID!) : {model_name} ID (Required)
""")
        for field in model_class._meta.get_fields():
            if field.name not in exceptions_update_fields and field.name != 'id':
                if isinstance(field, ForeignKey):
                    meta_file.write(f"- `{field.name}` (ID) : Related {field.related_model.__name__} ID\n")
                elif isinstance(field, JSONField):
                    meta_file.write(f"- `{field.name}` (JSONString) : JSON data for {field.name}\n")
                elif isinstance(field, (CharField, TextField)):
                    meta_file.write(f"- `{field.name}` (String) : {field.name.replace('_', ' ').title()}\n")
                elif isinstance(field, IntegerField):
                    meta_file.write(f"- `{field.name}` (Int) : {field.name.replace('_', ' ').title()}\n")
                elif isinstance(field, FloatField):
                    meta_file.write(f"- `{field.name}` (Float) : {field.name.replace('_', ' ').title()}\n")
                elif isinstance(field, BooleanField):
                    meta_file.write(f"- `{field.name}` (Boolean) : {field.name.replace('_', ' ').title()}\n")
                elif isinstance(field, DateField):
                    meta_file.write(f"- `{field.name}` (Date) : {field.name.replace('_', ' ').title()}\n")
                elif isinstance(field, DateTimeField):
                    meta_file.write(f"- `{field.name}` (DateTime) : {field.name.replace('_', ' ').title()}\n")

        meta_file.write(f"""
## **Returns:
- `success` (Boolean) : Indicates whether the operation was successful
- `message` (String) : Response message indicating success or failure
- `{nomenclature(model_name)}` ({model_name}Type) : Updated {model_name} object
- `errors` (String) : Error details if operation failed

---

## **Syntax
```graphql
mutation Update{model_name}(
    $id: ID!
""")
        for field in model_class._meta.get_fields():
            if field.name not in exceptions_update_fields and field.name != 'id':
                if isinstance(field, ForeignKey):
                    meta_file.write(f"    ${field.name}: ID\n")
                elif isinstance(field, JSONField):
                    meta_file.write(f"    ${field.name}: JSONString\n")
                elif isinstance(field, (CharField, TextField)):
                    meta_file.write(f"    ${field.name}: String\n")
                elif isinstance(field, IntegerField):
                    meta_file.write(f"    ${field.name}: Int\n")
                elif isinstance(field, FloatField):
                    meta_file.write(f"    ${field.name}: Float\n")
                elif isinstance(field, BooleanField):
                    meta_file.write(f"    ${field.name}: Boolean\n")
                elif isinstance(field, DateField):
                    meta_file.write(f"    ${field.name}: Date\n")
                elif isinstance(field, DateTimeField):
                    meta_file.write(f"    ${field.name}: DateTime\n")

        meta_file.write(f""") {{
    update{model_name}(
        id: $id
""")
        for field in model_class._meta.get_fields():
            if field.name not in exceptions_update_fields and field.name != 'id':
                meta_file.write(f"        {field.name}: ${field.name}\n")

        meta_file.write(f"""    ) {{
        success
        message
        {nomenclature(model_name)} {{
            id
""")
        for field in model_class._meta.get_fields():
            if not isinstance(field, (ManyToOneRel, ManyToManyRel)):
                field_name = field.name
                if field_name not in ['id']:
                    meta_file.write(f"            {field_name}\n")

        meta_file.write(f"""        }}
        errors
    }}
}}
```\"\"\"
""")


def generate_tests(model_name, model_class):
    model_dir = create_directories_and_files(model_name)
    file_path = os.path.join(model_dir, 'tests.py')
    print(f"Creating file: {file_path}")

    with open(file_path, 'w') as test_file:
        test_file.write(f"""import json
from django.test import TestCase
from graphene.test import Client
from ..schema import schema
from api import models

class {model_name}TestCase(TestCase):
    def setUp(self):
        # Create test data here
        self.test_instance = models.{model_name}.objects.create(
            # Add required fields here, e.g.:
            # field_name='value',
        )

    def test_query_{nomenclature(model_name)}(self):
        # Test querying {model_name}
        client = Client(schema)
        query = '''
        query {{
            {nomenclature(model_name)}List {{
                edges {{
                    node {{
                        id
                    }}
                }}
            }}
        }}
        '''
        executed = client.execute(query)
        self.assertIsNotNone(executed.get('data'))
        self.assertIn('{nomenclature(model_name)}List', executed.get('data'))

    def test_create_{nomenclature(model_name)}(self):
        # Test creating {model_name}
        client = Client(schema)
        mutation = '''
        mutation Create{model_name} {{
            create{model_name}(
                # Add required fields here, e.g.:
                # field_name: "value"
            ) {{
                success
                message
                {nomenclature(model_name)} {{
                    id
                }}
                errors
            }}
        }}
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['create{model_name}']['success'])
        self.assertIsNotNone(executed['data']['create{model_name}'][{model_name}.lower()]['id'])

    def test_update_{nomenclature(model_name)}(self):
        # Test updating {model_name}
        client = Client(schema)
        mutation = '''
        mutation Update{model_name} {{
            update{model_name}(
                id: self.test_instance.id,
                # Add fields to update here, e.g.:
                # field_name: "new_value"
            ) {{
                success
                message
                {nomenclature(model_name)} {{
                    id
                }}
                errors
            }}
        }}
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['update{model_name}']['success'])

    def test_delete_{nomenclature(model_name)}(self):
        # Test deleting {model_name}
        client = Client(schema)
        mutation = '''
        mutation Delete{model_name} {{
            delete{model_name}(
                id: self.test_instance.id
            ) {{
                success
                message
            }}
        }}
        '''
        executed = client.execute(mutation)
        self.assertIsNotNone(executed.get('data'))
        self.assertTrue(executed['data']['delete{model_name}']['success'])
""")


# Main script execution
for model_name, model_class in tables:
    if model_name not in exceptions_insert_fields:
        print(f"Processing {model_name}...")
        generate_types(model_name, model_class)
        generate_mutations(model_name, model_class)
        generate_queries(model_name)
        generate_meta(model_name, model_class)
        generate_tests(model_name, model_class)
        print(f"Completed {model_name}.")

# Create __init__.py files to make the modules importable
base_dir = os.path.join(script_dir, folder_name)
os.makedirs(base_dir, exist_ok=True)
with open(os.path.join(base_dir, '__init__.py'), 'w') as init_file:
    init_file.write("# This file makes the directory a Python package\n")

# Create schema.py to combine all queries and mutations
with open(os.path.join(base_dir, 'schema.py'), 'w') as schema_file:
    schema_file.write("""import graphene
from graphene import ObjectType

# Import all queries and mutations
""")
    for model_name, _ in tables:
        if model_name not in exceptions_insert_fields:
            schema_file.write(
                f"from .{nomenclature(model_name)} import mutations as {nomenclature(model_name)}_mutations,queries as {nomenclature(model_name)}_queries,{nomenclature(model_name)}_meta  \n")

    schema_file.write("\n\nclass Query(")
    query_classes = [f"{nomenclature(model_name)}_queries.{model_name}Query" for model_name, _ in tables if
                     model_name not in exceptions_insert_fields]
    schema_file.write(", ".join(query_classes))
    schema_file.write(", ObjectType):\n    pass\n\n")

    schema_file.write("class Mutation(ObjectType):\n")
    for model_name, _ in tables:
        if model_name not in exceptions_insert_fields:
            schema_file.write(
                f"    create_{nomenclature(model_name)} = {nomenclature(model_name)}_mutations.Create{model_name}.Field(description={nomenclature(model_name)}_meta.create_{nomenclature(model_name)})\n")
            schema_file.write(
                f"    update_{nomenclature(model_name)} = {nomenclature(model_name)}_mutations.Update{model_name}.Field(description={nomenclature(model_name)}_meta.update_{nomenclature(model_name)})\n")
            schema_file.write(
                f"    delete_{nomenclature(model_name)} = {nomenclature(model_name)}_mutations.Delete{model_name}.Field()\n")

    schema_file.write("\nschema = graphene.Schema(query=Query, mutation=Mutation)\n")

print("All models processed. Schema file created.")