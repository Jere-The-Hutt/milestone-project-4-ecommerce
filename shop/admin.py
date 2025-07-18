from django.contrib import admin
from .models import Product, CustomPackageRequest


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'price',
        'available',
        'created',
        'updated'
    ]
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CustomPackageRequest)
class CustomPackageRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'created']
    list_filter = ['created']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created']
    ordering = ['-created']
