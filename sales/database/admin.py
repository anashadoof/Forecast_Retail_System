from django.contrib import admin
from .models import Stores, Products, Promo, Sales

admin.site.register(Stores)
admin.site.register(Products)
admin.site.register(Promo)
admin.site.register(Sales)