from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Brand(BaseModel):
    name = models.CharField(max_length=255)


class Product(BaseModel):
    GENDER_CHOICES = (
        (1, 'male'),
        (2, 'female'),
        (3, 'boy'),
        (4, 'girl')
    )
    CATEGORIES_CHOICES = (
        (1, "Clothing"),
        (2, "Shoe"),
        (3, "Beauty"),
        (4, "Accessory")

    )
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
    categories = models.CharField(
        max_length=255, choices=CATEGORIES_CHOICES)  # model
    subcategories = models.CharField(max_length=255)  # model
    discount = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    collection = models.CharField(max_length=255, blank=True, null=True)


class FAQ(BaseModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()
