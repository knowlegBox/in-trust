import graphene
from django.core.exceptions import ValidationError
from api import models
from .types import TagType
from django.db import transaction


def get_instance_from_global_id(model, global_id, field_name):
    """Helper to get instance from global ID with proper error handling."""
    try:
        return model.objects.get(pk=global_id)
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid ID format for {field_name}")
    except model.DoesNotExist:
        raise ValidationError(f"{model.__name__} instance not found for {field_name}")


class CreateTag(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    tag = graphene.Field(TagType)

    class Arguments:
        id = graphene.Int()
        name = graphene.String()
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
            for field in models.Tag._meta.fields:  # Using fields only
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
            create_kwargs["added_by"] = models.Tag.objects.get(pk=kwargs['added_by'])
            instance = models.Tag.objects.create(**create_kwargs)
            return CreateTag(
                success=True,
                message="Tag created successfully",
                tag=instance
            )
        except ValidationError as e:
            return CreateTag(success=False, message=e.message)
        except Exception as e:
            return CreateTag(
                success=False, 
                message=f"Error creating Tag: {str(e)}"
            )


class UpdateTag(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    tag = graphene.Field(TagType)

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
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
            instance = models.Tag.objects.get(pk=id)

            # Update fields - only direct fields
            for field in models.Tag._meta.fields:
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
            instance.updated_by = models.Tag.objects.get(pk=kwargs['updated_by'])
            instance.full_clean()
            instance.save()
            return UpdateTag(
                success=True,
                message="Tag updated successfully",
                tag=instance
            )
        except models.Tag.DoesNotExist:
            return UpdateTag(
                success=False,
                message="Tag not found"
            )
        except ValidationError as e:
            return UpdateTag(success=False, message=e.message)
        except Exception as e:
            return UpdateTag(
                success=False, 
                message=f"Error updating Tag: {str(e)}"
            )


class DeleteTag(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, id):
        try:
            instance = models.Tag.objects.get(pk=id)
            instance.is_deleted=True
            instance._is_active=False
            instance.save()
            return DeleteTag(
                success=True,
                message="Tag deleted successfully"
            )
        except models.Tag.DoesNotExist:
            return DeleteTag(
                success=False,
                message="Tag not found"
            )
        except Exception as e:
            return DeleteTag(
                success=False,
                message=f"Error deleting Tag: {str(e)}"
            )

