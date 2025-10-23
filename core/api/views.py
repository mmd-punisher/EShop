from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import InStockFilterBackend, OrderFilter, ProductFilter
from api.models import Order, Product, User
from api.serializers import (
    OrderSerializer,
    ProductInfoSerializer,
    ProductSerializer,
    OrderCreateSerializer,
    UserSerializer,
)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(stock__gt=0).order_by("pk")
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend,
    ]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price", "stock"]
    pagination_class = LimitOffsetPagination
    # pagination_class = PageNumberPagination
    # pagination_class.page_size_query_param = "size"
    # pagination_class.max_page_size = 20

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        # or self.request.method == 'POST'
        if self.action == "create" or self.action == "update":
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    # Don't need
    # @action(detail=False, methods=["get"], url_path="user-order")
    # def user_order(self, request):
    #     orders = self.get_queryset().filter(
    #         user=request.user
    #     )  # reurn the queryset of the OrderViewSet
    #     serializer = self.get_serializer(orders, many=True)
    #     return Response(serializer.data)


class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer(
            {
                "products": products,
                "count": len(products),
                "max_price": products.aggregate(max_price=Max("price"))["max_price"],
            }
        )
        return Response(serializer.data)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
