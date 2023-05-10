from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('checkout/', views.checkout, name="checkout"),
    path('products/', views.product_search_page, name="products"),
    path('product/<str:pk>', views.single_product_page, name="product"),
]
