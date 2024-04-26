from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from api.models import Product
from api.serializers import ProductSerializer
# Create your views here.


class ProductListWith(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
