import graphene
from query_optimizer import DjangoConnectionField
from .types import ArticleType

class ArticleQuery(graphene.ObjectType):
    article = DjangoConnectionField(ArticleType)
