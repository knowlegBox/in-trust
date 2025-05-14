import graphene
from django.core.exceptions import ValidationError
from api import models
from .types import ArticleType
from django.db import transaction


def get_instance_from_global_id(model, global_id, field_name):
    """Helper to get instance from global ID with proper error handling."""
    try:
        return model.objects.get(pk=global_id)
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid ID format for {field_name}")
    except model.DoesNotExist:
        raise ValidationError(f"{model.__name__} instance not found for {field_name}")


class CreateArticle(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    article = graphene.Field(ArticleType)

    class Arguments:
        id = graphene.Int()
        title = graphene.String()
        slug = graphene.String()
        author = graphene.ID(required=True)
        content = graphene.String()
        is_private = graphene.Boolean()
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
            for field in models.Article._meta.fields:  # Using fields only
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
            create_kwargs["added_by"] = models.Article.objects.get(pk=kwargs['added_by'])
            instance = models.Article.objects.create(**create_kwargs)
            return CreateArticle(
                success=True,
                message="Article created successfully",
                article=instance
            )
        except ValidationError as e:
            return CreateArticle(success=False, message=e.message)
        except Exception as e:
            return CreateArticle(
                success=False, 
                message=f"Error creating Article: {str(e)}"
            )


class UpdateArticle(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    article = graphene.Field(ArticleType)

    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        slug = graphene.String()
        author = graphene.ID()
        content = graphene.String()
        is_private = graphene.Boolean()
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
            instance = models.Article.objects.get(pk=id)

            # Update fields - only direct fields
            for field in models.Article._meta.fields:
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
            instance.updated_by = models.Article.objects.get(pk=kwargs['updated_by'])
            instance.full_clean()
            instance.save()
            return UpdateArticle(
                success=True,
                message="Article updated successfully",
                article=instance
            )
        except models.Article.DoesNotExist:
            return UpdateArticle(
                success=False,
                message="Article not found"
            )
        except ValidationError as e:
            return UpdateArticle(success=False, message=e.message)
        except Exception as e:
            return UpdateArticle(
                success=False, 
                message=f"Error updating Article: {str(e)}"
            )


class DeleteArticle(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, id):
        try:
            instance = models.Article.objects.get(pk=id)
            instance.is_deleted=True
            instance._is_active=False
            instance.save()
            return DeleteArticle(
                success=True,
                message="Article deleted successfully"
            )
        except models.Article.DoesNotExist:
            return DeleteArticle(
                success=False,
                message="Article not found"
            )
        except Exception as e:
            return DeleteArticle(
                success=False,
                message=f"Error deleting Article: {str(e)}"
            )

