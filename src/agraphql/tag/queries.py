import graphene
from query_optimizer import DjangoConnectionField
from .types import TagType

class TagQuery(graphene.ObjectType):
    tag = DjangoConnectionField(TagType)
