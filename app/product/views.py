from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from product.models import Product
from product.serializers import ProductSerializer
from purchase.models import OrderItem
from django.db.models import Q

from drf_spectacular.utils import extend_schema
# Create your views here.


class ProductListView(APIView):
    permission_classes = [IsAuthenticated,]
    serializers_class = ProductSerializer

    @extend_schema(
        parameters=[
            {
                'name': 'price_min',
                'required': False,
                'in': 'query',
                'description': 'Minimum price filter',
                'schema': {'type': 'number'},
            },
            {
                'name': 'price_max',
                'required': False,
                'in': 'query',
                'description': 'Maximum price filter',
                'schema': {'type': 'number'},
            },
            {
                'name': 'color',
                'required': False,
                'in': 'query',
                'description': 'Color filter',
                'schema': {'type': 'string'},
            },
            {
                'name': 'brand',
                'required': False,
                'in': 'query',
                'description': 'Brand filter',
                'schema': {'type': 'string'},
            },
            {
                'name': 'parent_category',
                'required': False,
                'in': 'query',
                'description': 'Parent category filter',
                'schema': {'type': 'string'},
            },
            {
                'name': 'category',
                'required': False,
                'in': 'query',
                'description': 'Category filter',
                'schema': {'type': 'string'},
            },
            {
                'name': 'subcategory',
                'required': False,
                'in': 'query',
                'description': 'Subcategory filter',
                'schema': {'type': 'string'},
            },
            {
                'name': 'size',
                'required': False,
                'in': 'query',
                'description': 'Size filter',
                'schema': {'type': 'string'},
            },
            {
                'name': 'gender',
                'required': False,
                'in': 'query',
                'description': 'Gender filter',
                'schema': {'type': 'string'},
            },
        ]
    )
    def get(self, request):

        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')
        color = request.query_params.get('color')
        brand = request.query_params.get('brand')
        parent_category = request.query_params.get('parent_category')
        category = request.query_params.get('category')
        subcategory = request.query_params.get('subcategory')
        size = request.query_params.get('size')
        gender = request.query_params.get('gender')

        queryset = Product.objects.filter(number_of_products__gt=0)

        if price_min is not None:
            queryset = queryset.filter(price__gte=price_min)
        if price_max is not None:
            queryset = queryset.filter(price__lte=price_max)
        if color is not None:
            queryset = queryset.filter(color=color)
        if brand is not None:
            queryset = queryset.filter(brand__name=brand)
        if parent_category is not None:
            queryset = queryset.filter(parent_category__name=parent_category)
        if category is not None:
            queryset = queryset.filter(categories__name=category)
        if subcategory is not None:
            queryset = queryset.filter(subcategories__name=subcategory)
        if size is not None:
            queryset = queryset.filter(size=size)
        if gender is not None:
            queryset = queryset.filter(gender=gender)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ProductSerializer

    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET',])
def search_products(request):
    search_term = request.query_params.get('search_term')

    if search_term:
        queryset = Product.objects.filter(
            Q(name__icontains=search_term) | Q(
                brand__name__icontains=search_term)
        )

        queryset = queryset.filter(number_of_products__gt=0)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    else:
        return Response({'detail': 'Please provide a search term.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def top_sold_products(request):
    try:
        # Get all order items
        order_items = OrderItem.objects.all()

        # Dictionary to store sold quantities for each product
        product_sold_quantities = {}

        # Calculate sold quantities for each product
        for item in order_items:
            product_id = item.product.id
            if product_id in product_sold_quantities:
                product_sold_quantities[product_id] += item.quantity
            else:
                product_sold_quantities[product_id] = item.quantity

        # Sort products based on sold quantities in descending order
        sorted_products = sorted(
            product_sold_quantities.items(), key=lambda x: x[1], reverse=True)

        # Retrieve the top sold products (let's say top 10)
        top_sold_products = []
        for product_id, sold_quantity in sorted_products[:10]:
            product = Product.objects.get(id=product_id)
            top_sold_products.append({
                'product': ProductSerializer(product).data,
                'sold_quantity': sold_quantity
            })

        return Response(top_sold_products, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'No products sold'}, status=status.HTTP_404_NOT_FOUND)
