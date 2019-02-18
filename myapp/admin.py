from django.contrib import admin
from .models import Product, Demand, Position

admin.site.register(Product)
admin.site.register(Demand)
admin.site.register(Position)
