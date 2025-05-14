import graphene
from django.core.exceptions import ValidationError
from api import models
from .types import CategoryType
from django.db import transaction


def get_instance_from_global_id(model, global_id, field_name):
    """Helper to get instance from global ID with proper error handling."""
    try:
        return model.objects.get(pk=global_id)
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid ID format for {field_name}")
    except model.DoesNotExist:
        raise ValidationError(f"{model.__name__} instance not found for {field_name}")


class CreateCategory(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    category = graphene.Field(CategoryType)

    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        slug = graphene.String()
        active = graphene.Boolean()
        metas = graphene.JSONString(default_value=None)
        updated_by = graphene.ID(required=True)
        added_by = graphene.ID(required=True)
        status = graphene.Boolean()

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, **kwargs):
        try:
            # Convert foreign keys to instances
            create_kwargs = {}
            for field in models.Category._meta.fields:  # Using fields only
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
            create_kwargs["added_by"] = models.Category.objects.get(pk=kwargs['added_by'])
            instance = models.Category.objects.create(**create_kwargs)
            return CreateCategory(
                success=True,
                message="Category created successfully",
                category=instance
            )
        except ValidationError as e:
            return CreateCategory(success=False, message=e.message)
        except Exception as e:
            return CreateCategory(
                success=False, 
                message=f"Error creating Category: {str(e)}"
            )


class UpdateCategory(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    category = graphene.Field(CategoryType)

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        slug = graphene.String()
        active = graphene.Boolean()
        metas = graphene.JSONString()
        updated_by = graphene.ID()
        added_by = graphene.ID()
        is_deleted = graphene.Boolean()
        status = graphene.Boolean()

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, id, **kwargs):
        try:
            # Get instance
            instance = models.Category.objects.get(pk=id)

            # Update fields - only direct fields
            for field in models.Category._meta.fields:
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
            instance.updated_by = models.Category.objects.get(pk=kwargs['updated_by'])
            instance.full_clean()
            instance.save()
            return UpdateCategory(
                success=True,
                message="Category updated successfully",
                category=instance
            )
        except models.Category.DoesNotExist:
            return UpdateCategory(
                success=False,
                message="Category not found"
            )
        except ValidationError as e:
            return UpdateCategory(success=False, message=e.message)
        except Exception as e:
            return UpdateCategory(
                success=False, 
                message=f"Error updating Category: {str(e)}"
            )


class DeleteCategory(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, id):
        try:
            instance = models.Category.objects.get(pk=id)
            instance.is_deleted=True
            instance._is_active=False
            instance.save()
            return DeleteCategory(
                success=True,
                message="Category deleted successfully"
            )
        except models.Category.DoesNotExist:
            return DeleteCategory(
                success=False,
                message="Category not found"
            )
        except Exception as e:
            return DeleteCategory(
                success=False,
                message=f"Error deleting Category: {str(e)}"
            )

