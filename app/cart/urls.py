from django.urls import path
from cart.views import CartItemCreateAPIView, CartItemUpdateAPIView

urlpatterns = [
    path('', CartItemCreateAPIView.as_view(), name='create-cart'),
    path('update', CartItemUpdateAPIView.as_view(), name='update_cart'),
]
