from django.conf import settings
from django.db import models


class Item(models.Model):
    """Item that a user can buy"""
    title = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self) -> str:
        return self.title


class OrderItem(models.Model):
    """Item in the shopping cart relating to an item"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Order(models.Model):
    """Shopping cart per user"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username
