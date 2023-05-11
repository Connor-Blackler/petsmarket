from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import Item, Order, OrderItem
from django.utils import timezone

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


def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)

    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "item quantity was increased")
        else:
            messages.info(request, "item was added to the cart")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "new cart created, item was added to the cart")

    return redirect("product", pk=pk)


def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]

            order.items.remove(order_item)
            order.save()
            messages.info(request, "item was removed")
            return redirect("product", pk=pk)
        else:
            messages.info(request, "the order does not contain the item")
            return redirect("product", pk=pk)
    else:
        messages.info(request, "the user does not have an active order")
        return redirect("product", pk=pk)
