from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
            'billing_address',
            'billing_postal_code',
            'billing_city',
            'billing_country'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'billing_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Address (Optional)'}),
            'billing_postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code (Optional)'}),
            'billing_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City (Optional)'}),
            'billing_country': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'billing_address': 'Billing Address',
            'billing_postal_code': 'Postal Code',
            'billing_city': 'City',
            'billing_country': 'Country',
        }
