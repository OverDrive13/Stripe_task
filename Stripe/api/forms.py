from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """Форма для создания заказа."""
    class Meta:
        model = Order
        fields = ['items']
