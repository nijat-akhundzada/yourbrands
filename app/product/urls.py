from django.urls import path
from product.views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
]
