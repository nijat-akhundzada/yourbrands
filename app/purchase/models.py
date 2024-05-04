# from django.db import models
# from account.models import Address
# from cart.models import Cart

# # Create your models here.


# class Order(models.Model):
#     STATUS_CHOICES = (
#         ('it is being prepared', 'Hazırlanır'),
#         ('delivered', 'Təslim edildi'),
#         ('canceled', 'Ləğv edildi'),
#     )
#     product_in_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE)
#     delivery_type = models.CharField(max_length=255)
#     payment_type = models.CharField(max_length=255)
#     order_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     additional_notes = models.TextField()
#     status = models.CharField(max_length=255, choices=STATUS_CHOICES)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


# class OrderRatingImage(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     order_rating_image = models.ImageField(upload_to='order_rating_images')


# class OrderRating(models.Model):
#     order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
#     rate = models.IntegerField()
#     user_thought = models.TextField()


# class CanceledOrder(models.Model):
#     order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
#     reason = models.CharField(max_length=255)
#     additional_notes = models.TextField()
