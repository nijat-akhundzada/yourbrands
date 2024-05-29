from rest_framework import serializers
from product.models import Product, ProductImages, Brand, BrandWithImage


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ('id', 'image')


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'brand', 'images')

    def get_discounted_price(self, obj):
        return obj.discounted_price()


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'logo')


class BrandWithImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandWithImage
        fields = ('id', 'name', 'image', 'gender')
        read_only_fields = ['name', 'image']
