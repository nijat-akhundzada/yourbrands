from django.contrib import admin
from product.models import Brand, ParentCategory, Category, Product, ProductImages, Subcategory, Gender, BrandWithImage
# Register your models here.
admin.site.register(Brand)
admin.site.register(ParentCategory)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(Subcategory)
admin.site.register(Gender)
admin.site.register(BrandWithImage)
