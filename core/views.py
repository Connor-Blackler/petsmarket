from django.shortcuts import render
from .models import Item

# Create your views here.


def home_page(request):
    context = {}

    return render(request, "home-page.html", context)


def checkout(request):
    context = {}

    return render(request, "checkout-page.html", context)


def product_search_page(request):
    context = {
        "items": Item.objects.all()
    }

    return render(request, "product-search-page.html", context)


def single_product_page(request, pk):
    context = {
        "item": Item.objects.all()
    }

    return render(request, "product-page.html", context)
