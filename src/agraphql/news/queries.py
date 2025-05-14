import graphene
from query_optimizer import DjangoConnectionField
from .types import NewsType

class NewsQuery(graphene.ObjectType):
    news = DjangoConnectionField(NewsType)
