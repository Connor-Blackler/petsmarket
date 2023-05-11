from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('checkout/', views.checkout, name="checkout"),
    path('products/', views.ProductSearchView.as_view(), name="products"),
    path('product/<str:pk>/', views.ProductView.as_view(), name="product"),
    path("add-to-cart/<str:pk>/", views.add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<str:pk>/",
         views.remove_from_cart, name="remove-from-cart"),
]
