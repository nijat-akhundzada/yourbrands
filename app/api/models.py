from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Brand(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ParentCategory(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey(
        ParentCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'Parent category: {self.parent_category}, category: {self.name}'


class Subcategory(BaseModel):
    name = models.CharField(models.Model)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'Category: {self.category}, subcategory: {self.name}'


class Size(models.Model):
    size = models.CharField(max_length=255)

    def __str__(self):
        return self.size


class Color(models.Model):
    color = models.CharField(max_length=255)

    def __str__(self):
        return self.color


class Product(BaseModel):
    GENDER_CHOICES = (
        (1, 'male'),
        (2, 'female'),
        (3, 'boy'),
        (4, 'girl')
    )
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, blank=True, null=True)
    parent_category = models.ForeignKey(
        ParentCategory, on_delete=models.CASCADE, blank=True, null=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True
                                   )
    subcategories = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, blank=True, null=True)
    discount = models.FloatField()  # ?
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    collection = models.CharField(max_length=255, blank=True, null=True)
    product_code = models.CharField(max_length=255, blank=True, null=True)  # ?

    def __str__(self):
        return f'{self.name},{self.brand}'


class ProductImages(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return self.product


class FAQ(BaseModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()


class TermAndCondition(BaseModel):
    terms_and_conditions = models.TextField()

    def __str__(self):
        return 'Our Terms&Conditions'


class PrivacyPolicy(BaseModel):
    privacy_policy = models.TextField()

    def __str__(self):
        return 'Our Privacy Policy'
