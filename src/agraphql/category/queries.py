import graphene
from query_optimizer import DjangoConnectionField
from .types import CategoryType

class CategoryQuery(graphene.ObjectType):
    category = DjangoConnectionField(CategoryType)
