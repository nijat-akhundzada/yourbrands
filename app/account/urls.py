from django.urls import path
from account.views import (CustomUserListCreateAPIView, CustomUserDetailAPIView,
                           send_otp, change_password, reset_password, WishlistView)

app_name = 'account'

urlpatterns = [
    path('users/', CustomUserListCreateAPIView.as_view(), name='list_users'),
    path('user/<int:pk>', CustomUserDetailAPIView.as_view(), name='user_detail'),
    path('send-otp/', send_otp, name='send_otp'),
    path('change-password/', change_password, name='change_password'),
    path('reset-password/', reset_password, name='reset_password'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),

]