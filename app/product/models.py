from django.db import models

from datetime import timedelta
from django.utils import timezone
# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Gender(models.Model):
    GENDER_CHOICES = (
        ('Men', 'Kişilər'),
        ('Women', 'Qadınlar'),
        ('Boys', 'Oğlanlar'),
        ('Girls', 'Qızlar'),
    )
    type = models.CharField(
        max_length=255, choices=GENDER_CHOICES, unique=True)

    def __str__(self):
        return self.type


class Brand(BaseModel):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='brand_logos', blank=True, null=True)

    def __str__(self):
        return self.name


class ParentCategory(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    gender = models.ManyToManyField(Gender, related_name='parent_categories')

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    parent_category = models.ManyToManyField(
        ParentCategory, related_name='categories')
    gender = models.ManyToManyField(Gender, related_name='categories')

    def __str__(self):
        return self.name


class Subcategory(BaseModel):
    name = models.CharField(models.Model)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'Category: {self.category}, subcategory: {self.name}'


class Product(BaseModel):
    name = models.CharField(max_length=255)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, blank=True, null=True)
    parent_category = models.ForeignKey(
        ParentCategory, on_delete=models.CASCADE, blank=True, null=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True
                                   )
    subcategories = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, blank=True, null=True)
    discount = models.FloatField(
        default=0.0, help_text="Enter discount percentage for the product.")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255)
    collection = models.CharField(max_length=255, blank=True, null=True)
    product_code = models.CharField(max_length=255, blank=True, null=True)
    number_of_views = models.IntegerField(default=0)
    stock = models.IntegerField(default=1)

    def discounted_price(self):
        self.price = self.price - self.price * (1 - self.discount / 100)

    def is_new(self):
        new_threshold = timedelta(days=30)

        threshold_date = timezone.now() - new_threshold

        return self.created_at >= threshold_date

    def __str__(self):
        return f'{self.name},{self.brand}'


class ProductImages(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return self.product
