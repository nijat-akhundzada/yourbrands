from django.urls import path
from .views import ProductListView, ProductDetailView, search_products, top_sold_products, get_brands, SimilarProductsView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('search/', search_products, name='product-search'),
    path('top-sold/', top_sold_products, name='top-sold-products'),
    path('get-brands/', get_brands, name='get-brands'),
    path('similar/', SimilarProductsView.as_view(),
         name='similar-products'),
]
