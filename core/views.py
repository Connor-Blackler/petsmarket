from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item

# Create your views here.


def home_page(request):
    context = {}

    return render(request, "home-page.html", context)


def checkout(request):
    context = {}

    return render(request, "checkout-page.html", context)


class ProductSearchView(ListView):
    model = Item
    template_name = "product-search-page.html"


class ProductView(DetailView):
    model = Item
    template_name = "product-page.html"
