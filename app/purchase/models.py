from django.db import models
from account.models import Address

# Create your models here.


class Order(models.Model):
    delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    delivery_type = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=255)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    additional_notes = models.TextField()
    status = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_payment():
        pass


class OrderRatingImage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_rating_image = models.ImageField(upload_to='order_rating_images')


class OrderRating(models.Model):
    order = models.ForeignKey(Order)
    rate = models.IntegerField()
    user_thought = models.TextField()
