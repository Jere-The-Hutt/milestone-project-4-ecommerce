from django import forms
from .models import CustomPackageRequest


class CustomPackageRequestForm(forms.ModelForm):
    class Meta:
        model = CustomPackageRequest
        fields = ['name', 'email', 'phone', 'message']
