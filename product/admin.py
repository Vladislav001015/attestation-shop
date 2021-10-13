from django.contrib import admin

from product.models import Product, Category, Like
from django.contrib import admin
from .models import Contact


admin.site.register(Like)

admin.site.register(Product)
admin.site.register(Category)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
