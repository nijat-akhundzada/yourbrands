from django.urls import path
from api.views import ProductListWith

urlpatterns = [
    path('products/', ProductListWith.as_view(), name='list-products'),
]
