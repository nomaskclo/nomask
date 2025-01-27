from django.contrib import admin
from .models import Product, Cart, CartObject, AccessRequest, Payment
# Register your models here.

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartObject)
admin.site.register(AccessRequest)
admin.site.register(Payment)