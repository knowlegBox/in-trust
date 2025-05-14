from query_optimizer import DjangoObjectType, filter
from api import models
import django_filters
import graphene


class CategoryFilter(django_filters.FilterSet):
    order_by = django_filters.OrderingFilter(
        fields=(
            [
                field.name + "__id" if field.is_relation else field.name
                for field in models.Category._meta.fields
            ]
        )
    )
    id__exclude_in = django_filters.ModelMultipleChoiceFilter(
        queryset=models.Category.objects,
        method='filter_id_exclude',
    )

    def filter_id_exclude(self, queryset, name, value):
        if value:
            exclude_ids = [obj.id for obj in value]
            return queryset.exclude(id__in=exclude_ids)
        return queryset

    class Meta:
        model = models.Category
        fields = {field.name + "__id" if field.is_relation else field.name: ["exact", "in"] for field in
                  models.Category._meta.fields}
        exclude = ['metas']

class CategoryType(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)

    class Meta:
        model = models.Category
        filterset_class = CategoryFilter
        interfaces = (graphene.relay.Node,)
