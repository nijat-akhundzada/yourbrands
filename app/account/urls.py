from django.urls import path
from account.views import CustomUserListCreateAPIView, CustomUserDetailAPIView, send_otp

app_name = 'account'

urlpatterns = [
    path('users/', CustomUserListCreateAPIView.as_view(), name='list_users'),
    path('user/<int:pk>', CustomUserDetailAPIView.as_view(), name='user_detail'),
    path('send-otp/', send_otp, name='send_otp'),
]
