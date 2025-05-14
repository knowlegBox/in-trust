import graphene
from query_optimizer import DjangoConnectionField
from .types import ProfileType

class ProfileQuery(graphene.ObjectType):
    profile = DjangoConnectionField(ProfileType)
