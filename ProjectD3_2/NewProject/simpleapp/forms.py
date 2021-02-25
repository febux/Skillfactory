from django.forms import ModelForm, BooleanField  # Импортируем true-false поле
from .models import Product


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'quantity']
