from django.urls import path
from detail.views import send_otp, check_otp, get_offers, get_statuses

urlpatterns = [
    path('send-otp/', send_otp, name='send_otp'),
    path('check-otp/', check_otp, name='check_otp'),
    path('get-offers', get_offers),
    path('get-statuses', get_statuses),
]
