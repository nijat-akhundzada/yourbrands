from django.urls import path
from product.views import ProductListView, ProductDetailView, top_sold_products

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('best_sold', top_sold_products),
]
