from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='orders'
    )
    product = models.ForeignKey(
        Product,
        related_name='orders',
        on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
        )

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id} - {self.product.name}'

    def get_total_cost(self):
        return self.product.price

    def get_stripe_url(self):
        if not self.stripe_id:
            # no payment associated
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # Stripe path for test payments
            path = '/test/'
        else:
            # Stripe path for real payments
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
