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
    print(request.user.is_authenticated)
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
        else:
            order.items.add(order_item)

        messages.info(
            request, f"{order_item.quantity} '{order_item.item.title}' is now in your cart")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(
            request, f"new cart created, {order_item.quantity} '{order_item.item.title}' is now in your cart")

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

            order_item.quantity -= 1
            order_item.save()
            if order_item.quantity == 0:
                order.items.remove(order_item)
                order_item.delete()
                messages.info(
                    request, f"'{order_item.item.title}' is no longer in your cart")

            else:
                messages.info(
                    request, f"{order_item.quantity} '{order_item.item.title}' is now in your cart")

            return redirect("product", pk=pk)
        else:
            messages.info(
                request, f"This item is not in your cart")
            return redirect("product", pk=pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", pk=pk)
