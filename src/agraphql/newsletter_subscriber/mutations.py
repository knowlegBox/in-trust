import graphene
from django.core.exceptions import ValidationError
from api import models
from .types import NewsletterSubscriberType
from django.db import transaction


def get_instance_from_global_id(model, global_id, field_name):
    """Helper to get instance from global ID with proper error handling."""
    try:
        return model.objects.get(pk=global_id)
    except (TypeError, ValueError):
        raise ValidationError(f"Invalid ID format for {field_name}")
    except model.DoesNotExist:
        raise ValidationError(f"{model.__name__} instance not found for {field_name}")


class CreateNewsletterSubscriber(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    newsletter_subscriber = graphene.Field(NewsletterSubscriberType)

    class Arguments:
        id = graphene.Int()
        email = graphene.String()
        subscribed_at = graphene.DateTime()
        is_confirmed = graphene.Boolean()
        confirmation_token = graphene.String()
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
            for field in models.NewsletterSubscriber._meta.fields:  # Using fields only
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
            create_kwargs["added_by"] = models.NewsletterSubscriber.objects.get(pk=kwargs['added_by'])
            instance = models.NewsletterSubscriber.objects.create(**create_kwargs)
            return CreateNewsletterSubscriber(
                success=True,
                message="NewsletterSubscriber created successfully",
                newsletter_subscriber=instance
            )
        except ValidationError as e:
            return CreateNewsletterSubscriber(success=False, message=e.message)
        except Exception as e:
            return CreateNewsletterSubscriber(
                success=False, 
                message=f"Error creating NewsletterSubscriber: {str(e)}"
            )


class UpdateNewsletterSubscriber(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    newsletter_subscriber = graphene.Field(NewsletterSubscriberType)

    class Arguments:
        id = graphene.ID(required=True)
        email = graphene.String()
        subscribed_at = graphene.DateTime()
        is_confirmed = graphene.Boolean()
        confirmation_token = graphene.String()
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
            instance = models.NewsletterSubscriber.objects.get(pk=id)

            # Update fields - only direct fields
            for field in models.NewsletterSubscriber._meta.fields:
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
            instance.updated_by = models.NewsletterSubscriber.objects.get(pk=kwargs['updated_by'])
            instance.full_clean()
            instance.save()
            return UpdateNewsletterSubscriber(
                success=True,
                message="NewsletterSubscriber updated successfully",
                newsletter_subscriber=instance
            )
        except models.NewsletterSubscriber.DoesNotExist:
            return UpdateNewsletterSubscriber(
                success=False,
                message="NewsletterSubscriber not found"
            )
        except ValidationError as e:
            return UpdateNewsletterSubscriber(success=False, message=e.message)
        except Exception as e:
            return UpdateNewsletterSubscriber(
                success=False, 
                message=f"Error updating NewsletterSubscriber: {str(e)}"
            )


class DeleteNewsletterSubscriber(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, id):
        try:
            instance = models.NewsletterSubscriber.objects.get(pk=id)
            instance.is_deleted=True
            instance._is_active=False
            instance.save()
            return DeleteNewsletterSubscriber(
                success=True,
                message="NewsletterSubscriber deleted successfully"
            )
        except models.NewsletterSubscriber.DoesNotExist:
            return DeleteNewsletterSubscriber(
                success=False,
                message="NewsletterSubscriber not found"
            )
        except Exception as e:
            return DeleteNewsletterSubscriber(
                success=False,
                message=f"Error deleting NewsletterSubscriber: {str(e)}"
            )

