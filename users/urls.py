from django.urls import path, include
from . import views
from core.views import home_page

urlpatterns = [
    path('', include('allauth.urls')),
    path("my-profile/", views.my_profile, name="user-account"),
]
