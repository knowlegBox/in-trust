import graphene
from query_optimizer import DjangoConnectionField
from .types import ContactMessageType

class ContactMessageQuery(graphene.ObjectType):
    contact_message = DjangoConnectionField(ContactMessageType)
