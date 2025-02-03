from django import forms
from django.forms import ModelForm
from home.models import DeliveryPriceByRegion, ProductStock, Payment
from .models import Accessible


class DeliveryPriceForm(ModelForm):
    class Meta:
        model = DeliveryPriceByRegion
        exclude = ['name', 'delivery_method']

class AccessibleForm(ModelForm):
    class Meta:
        model = Accessible
        fields = ['access']

class ProductStockForm(forms.ModelForm):
    class Meta:
        model = ProductStock
        fields = [
            'reflectorBlack',
            'reflectorGrey',
            'relectorWhite',   # Change to 'reflectorWhite' if needed.
            'reflectorPeach',
            'reflectorTPS',
            'ogBlack',
            'ogGrey',
        ]
        labels = {
            'reflectorBlack': 'NoMask Reflector Black',
            'reflectorGrey': 'NoMask Reflector Grey',
            'relectorWhite': 'NoMask Reflector White',
            'reflectorPeach': 'NoMask Reflector Peach',
            'reflectorTPS': 'NoMask Reflector Tree Pattern Skully',
            'ogBlack': 'NoMask OG Black',
            'ogGrey': 'NoMask OG Grey',
        }

class DeliveryStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['delivered']

        