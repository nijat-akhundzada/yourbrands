from django.urls import path
from purchase.views import OrderListCreateAPIView, CanceledOrderCreateAPIView

urlpatterns = [
    path('order', OrderListCreateAPIView.as_view(), name='create_order'),
    path('cancel-order', CanceledOrderCreateAPIView.as_view(), name='cancel_order'),
]
