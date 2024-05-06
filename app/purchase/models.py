from django.db import models
from account.models import CustomUser
from address.models import Address
from product.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('Processing', 'Hazırlanır'),
        ('Delivered', 'Təslim edildi'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Processing')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True)
    additional_notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.mobile_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem #{self.id} in Order #{self.order.id}"


class CanceledOrder(models.Model):
    order = models.ForeignKey(OrderItem, on_delete=models.SET_NULL)
    reason = models.CharField(max_length=255)
    additional_notes = models.TextField()

    # class OrderRatingImage(models.Model):
    #     order = models.ForeignKey(Order, on_delete=models.CASCADE)
    #     order_rating_image = models.ImageField(upload_to='order_rating_images')

    # class OrderRating(models.Model):
    #     order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    #     rate = models.IntegerField()
    #     user_thought = models.TextField()
