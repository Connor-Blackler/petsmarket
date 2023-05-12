from users.models import Profile
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
import uuid
import math


UI_FLAG_CHOICES = (
    ("primary", "blue"),
    ("secondary", "grey"),
    ("danger", "red"),
    ("success", "green"),
    ("dark", "black"),
)


class AuthenticationBackendAnonymous:
    '''
            This is for automatically signing in the user after signup etc.
    '''

    def authenticate(self, user=None):
        # make sure they have a profile and that they are anonymous
        # if you're not using profiles you can just return user
        if not user.get_profile() or not user.get_profile().anonymous:
            user = None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class Label(models.Model):
    """A Label category used to associate with products"""
    title = models.CharField(max_length=100)
    ui_flag = models.CharField(choices=UI_FLAG_CHOICES, max_length=100)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    """A main category used to associate with products"""
    title = models.CharField(max_length=100)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.title


class SubCategory(models.Model):
    """A subcategory used to associate with products"""
    title = models.CharField(max_length=100)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.title


class Discount(models.Model):
    """A Discount used to associate with products"""
    discount_amount = models.PositiveIntegerField(
        default=15, validators=[MinValueValidator(5), MaxValueValidator(50)])
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return str(self.discount_amount)

    def apply_discount(self, price: float) -> float:
        return price * (1 - self.discount_amount / 100.0)


class Item(models.Model):
    """Item that a user can buy"""
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount = models.ForeignKey(
        Discount, blank=True, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"pk": self.pk})

    def get_discounted_price(self):
        if self.discount:
            return round(math.ceil(self.discount.apply_discount(self.price)) - 0.01, 2)
        else:
            return self.price


class OrderItem(models.Model):
    """Item in the shopping cart relating to an item"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.quantity} of {self.item.title}"


class Order(models.Model):
    """Shopping cart per user"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.user.username
