from django.urls import path
from detail.views import send_otp, check_otp

urlpatterns = [
    path('send-otp/', send_otp, name='send_otp'),
    path('check-otp/', check_otp, name='check_otp'),
]
