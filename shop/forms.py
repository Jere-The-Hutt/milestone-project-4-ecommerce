from django import forms
from .models import CustomPackageRequest


class CustomPackageRequestForm(forms.ModelForm):
    class Meta:
        model = CustomPackageRequest
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email address',
                'class': 'form-control',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone number (optional)',
                'class': 'form-control',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Describe your custom project needs',
                'class': 'form-control',
                'rows': 5,
            }),
        }
