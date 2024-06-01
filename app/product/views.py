from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from product.models import Product, Brand, BrandWithImage
from product.serializers import ProductSerializer, BrandSerializer, BrandWithImageSerializer
from purchase.models import OrderItem
from django.db.models import Q


from drf_spectacular.utils import extend_schema, OpenApiParameter
# Create your views here.


class ProductsPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(
    parameters=[
        OpenApiParameter(name='price_min', type=int,
                         location='query', description='Minimum price filter'),
        OpenApiParameter(name='price_max', type=int,
                         location='query', description='Maximum price filter'),
        OpenApiParameter(name='color', type=str,
                         location='query', description='Color filter'),
        OpenApiParameter(name='brand', type=str,
                         location='query', description='Brand filter'),
        OpenApiParameter(name='parent_category', type=str,
                         location='query', description='Parent category filter'),
        OpenApiParameter(name='category', type=str,
                         location='query', description='Category filter'),
        OpenApiParameter(name='subcategory', type=str,
                         location='query', description='Subcategory filter'),
        OpenApiParameter(name='size', type=str,
                         location='query', description='Size filter'),
        OpenApiParameter(name='gender', type=str,
                         location='query', description='Gender filter'),
        OpenApiParameter(name='page', type=int, location='query',
                         description='Page number for pagination'),
        OpenApiParameter(name='page_size', type=int, location='query',
                         description='Number of items per page')
    ]
)
class ProductListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination

    def get_queryset(self):
        request = self.request

        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')
        color = request.query_params.get('color')
        brand = request.query_params.get('brand')
        parent_category = request.query_params.get('parent_category')
        category = request.query_params.get('category')
        subcategory = request.query_params.get('subcategory')
        size = request.query_params.get('size')
        gender = request.query_params.get('gender')

        try:
            queryset = Product.objects.filter(stock__gt=0)
        except:
            queryset = []

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

        return queryset


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


class SimilarProductsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(name='id', type=int, location='query',
                             description='ID of the product to find similar items for'),
            OpenApiParameter(name='page', type=int, location='query',
                             description='Page number for pagination'),
            OpenApiParameter(name='page_size', type=int, location='query',
                             description='Number of items per page')
        ]
    )
    def get(self, request):
        product_id = request.query_params.get('id')
        if not product_id:
            return Response({'detail': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        similar_products = Product.objects.filter(
            subcategories__in=product.subcategories.all(),
            categories__in=product.categories.all(),
        ).exclude(id=product_id)  # Exclude the current product

        paginator = ProductsPagination()
        paginated_products = paginator.paginate_queryset(
            similar_products, request)
        serializer = ProductSerializer(paginated_products, many=True)

        return paginator.get_paginated_response(serializer.data)


@api_view(['GET',])
def search_products(request):
    search_term = request.query_params.get('search_term')

    if search_term:
        queryset = Product.objects.filter(
            Q(name__icontains=search_term) | Q(
                brand__name__icontains=search_term)
        )

        queryset = queryset.filter(number_of_products__gt=0)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
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

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(top_sold_products, request)
        return paginator.get_paginated_response(result_page)
    except:
        return Response({'message': 'No products sold'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_brands(request):
    brands = Brand.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(brands, request)
    serializer = BrandSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@extend_schema(request=BrandWithImageSerializer)
@api_view(['POST'])
def get_brands_with_images(request):
    gender = request.data.get('gender')
    if gender:
        filtered_brands = BrandWithImage.objects.filter(gender=gender)
        serializer = BrandWithImageSerializer(filtered_brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'Gender not provided'}, status=status.HTTP_400_BAD_REQUEST)
