from django.contrib import admin
from core.models import *


# Register your models here.
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Label)
admin.site.register(Discount)
