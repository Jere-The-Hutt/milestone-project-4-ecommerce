from django.contrib import admin
from .models import Order
from django.utils.safestring import mark_safe


def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''


order_payment.short_description = 'Stripe payment'


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
        order_payment,
        'created',
        'updated'
    ]
    list_filter = ['paid', 'created', 'updated']
