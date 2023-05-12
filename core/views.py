from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from .models import Item, Order, OrderItem
from django.http import HttpResponse
from django.utils import timezone
from users.models import Profile
import uuid

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


def anonymous_or_real(request, response):
    # do we have an existing user?
    if request.user.is_authenticated:
        return request.user
    else:
        u = None
        try:
            my_cookie_value = request.COOKIES.get('user-anon-id')
            if my_cookie_value:
                print("my cookie value is " + my_cookie_value)
                u = User.objects.get(id=my_cookie_value)
                print("my cookie user is: " + str(u is None))
            else:
                print("cookie is none")
        except KeyError:
            ...

        if u is None:
            print("User is none: creating anon user")
            username = str(uuid.uuid4())
            u = User(username=username,
                     first_name='Anonymous', last_name='User')
            u.set_unusable_password()
            u.save()

            u.username = u.id
            u.save()

            try:
                p = Profile.objects.get(user=u)
            except Profile.DoesNotExist:
                p = Profile(user=u, anonymous=True)
                p.save()

            response.set_cookie('user-anon-id', u.id)
            print(f"creating anon user: {u.id}")

        backend = 'core.models.AuthenticationBackendAnonymous'
        user = authenticate(user=u, backend=backend)
        print(f"user is none?: {user is None}")
        print(f"u is none?: {u is None}")
        if user is not None:
            login(request, u, backend=backend)
        return u


def add_to_cart(request, pk):
    ret = redirect("product", pk=pk)
    item = get_object_or_404(Item, pk=pk)
    print(request.user)
    my_user = anonymous_or_real(request, ret)
    print(my_user.is_authenticated)

    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=my_user,
        ordered=False)

    order_qs = Order.objects.filter(
        user=my_user,
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
            user=my_user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(
            request, f"new cart created, {order_item.quantity} '{order_item.item.title}' is now in your cart")

    return ret


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
