from django.contrib import admin
from .models import Product, Cart, ContactData,CartObject, AccessRequest, Payment, DeliveryPriceByRegion, ProductStock
# Register your models here.

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartObject)
admin.site.register(AccessRequest)
admin.site.register(Payment)
admin.site.register(DeliveryPriceByRegion)
admin.site.register(ProductStock)
admin.site.register(ContactData)