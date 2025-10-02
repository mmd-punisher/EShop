import django_filters
from api.models import Product, Order
from rest_framework import filters


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["iexact", "icontains"],
            "price": ["exact", "lt", "gt", "range"],
        }


class OrderFilter(django_filters.FilterSet):
    # orders/?created_at=2024-03-18
    created_at = django_filters.DateFilter(field_name="created_at__date")

    class Meta:
        model = Order
        fields = {
            "status": ["iexact", "icontains"],
            "created_at": ["exact", "lt", "gt", "range"],
        }


class InStockFilterBackend(filters.BaseFilterBackend):
    """
    Filter items that are in stock
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)
