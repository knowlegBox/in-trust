from query_optimizer import DjangoObjectType, filter
from api import models
import django_filters
import graphene


class ProfileFilter(django_filters.FilterSet):
    order_by = django_filters.OrderingFilter(
        fields=(
            [
                field.name + "__id" if field.is_relation else field.name
                for field in models.Profile._meta.fields
            ]
        )
    )
    id__exclude_in = django_filters.ModelMultipleChoiceFilter(
        queryset=models.Profile.objects,
        method='filter_id_exclude',
    )

    def filter_id_exclude(self, queryset, name, value):
        if value:
            exclude_ids = [obj.id for obj in value]
            return queryset.exclude(id__in=exclude_ids)
        return queryset

    class Meta:
        model = models.Profile
        fields = {field.name + "__id" if field.is_relation else field.name: ["exact", "in"] for field in
                  models.Profile._meta.fields}
        exclude = ['metas']

class ProfileType(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)

    class Meta:
        model = models.Profile
        filterset_class = ProfileFilter
        interfaces = (graphene.relay.Node,)
