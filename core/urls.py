from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('checkout/', views.checkout, name="checkout"),
    path('products/', views.ProductSearchView.as_view(), name="products"),
    path('product/<str:pk>/', views.ProductView.as_view(), name="product"),
]
