from django import forms
from django.forms import ModelForm
from home.models import DeliveryPriceByRegion
from .models import Accessible

class DeliveryPriceForm(ModelForm):
    class Meta:
        model = DeliveryPriceByRegion
        exclude = ['name', 'delivery_method']

class AccessibleForm(ModelForm):
    class Meta:
        model = Accessible
        fields = ['access']