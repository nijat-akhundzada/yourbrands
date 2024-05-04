from django.urls import path
from account.views import (CustomUserListCreateAPIView, CustomUserDetailAPIView, WishlistView,
                           change_password, reset_password)

app_name = 'account'

urlpatterns = [
    path('users/', CustomUserListCreateAPIView.as_view(), name='list_users'),
    path('user/<int:pk>', CustomUserDetailAPIView.as_view(), name='user_detail'),
    path('change-password/', change_password, name='change_password'),
    path('reset-password/', reset_password, name='reset_password'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
]
