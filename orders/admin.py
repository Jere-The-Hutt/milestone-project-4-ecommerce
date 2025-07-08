from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'billing_address',
        'billing_postal_code',
        'billing_city',
        'billing_country',
        'paid',
        'created',
        'updated'
    ]
    list_filter = ['paid', 'created', 'updated']
