import graphene
from query_optimizer import DjangoConnectionField
from .types import NewsletterSubscriberType

class NewsletterSubscriberQuery(graphene.ObjectType):
    newsletter_subscriber = DjangoConnectionField(NewsletterSubscriberType)
