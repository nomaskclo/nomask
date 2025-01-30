from django import forms
from django.forms import ModelForm
from home.models import DeliveryPriceByRegion

class DeliveryPriceForm(ModelForm):
    class Meta:
        model = DeliveryPriceByRegion
        exclude = ['name', 'delivery_method']