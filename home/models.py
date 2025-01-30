import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class AccessRequest(models.Model):
    unique_id = models.UUIDField(unique=True,editable=False,default=uuid.uuid4)
    email = models.CharField(max_length=255,null=True,blank=True)
    username = models.CharField(max_length=255,null=True,blank=True)
    password = models.CharField(max_length=255,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    granted = models.BooleanField(default=False)


    def __str__(self):
        return self.email
    
class Product(models.Model):   
    name = models.CharField(max_length=255)
    unique_id = models.CharField(max_length=255,null=True,blank=True)
    imageUrl = models.CharField(max_length=255,null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    is_active = models.BooleanField(default=True)
    ogStock = models.PositiveIntegerField(default=0)
    reflectorStock = models.PositiveIntegerField(default=0)
    
    @property
    def discount_percentage(self):
        """
        Calculates the discount percentage based on old price (discount_price) and new price.
        Returns the discount percentage as an integer (rounded).
        """
        if self.discount_price and self.price and self.discount_price > self.price:
            discount = ((self.discount_price - self.price) / self.discount_price) * 100
            return round(discount)  # Returns an integer discount percentage
        return 0  # Return 0 if no discount applies
    
    

    def __str__(self):
        return self.name
    




class Payment(models.Model):
    # personal details 
    unique_id = models.UUIDField(unique=True,editable=False,default=uuid.uuid4)
    first_name = models.CharField(max_length=255,blank=True)
    last_name = models.CharField(max_length=255,blank=True)
    country_code = models.CharField(max_length=255)
    phone = models.CharField(max_length=255,blank=True)
    email = models.EmailField(blank=True)
    order_notes = models.TextField(blank=True)

    # delivery Address
    street_address_1 = models.CharField(max_length=255, verbose_name='Street Address Line 1', null=True)
    street_address_2 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Street Address Line 2 (optional)')
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, null=True)
    destination_country = models.CharField(max_length=100, null=True)
    accralocation = models.CharField(max_length=255,null=True,blank=True)
    

    additional_info = models.TextField(blank=True)

    # cart and payment
    amount = models.FloatField(blank=True, null=True)

    ref = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
   
    verified = models.BooleanField(default=False)
    delivery_price = models.IntegerField(default=0)
    delivered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    pickupdata = models.BooleanField(default=False)
    

    class Meta:
        ordering = ('-date_created',)

    def __str__(self) -> str:
        return f'Payment: {self.amount}'

    @property
    def get_formatted_address(self):
        """
        Returns a nicely formatted delivery address for display purposes.
        """
        address_lines = [
            self.street_address_1,
            self.street_address_2,
            f"{self.city}, {self.state} {self.zip_code}" if self.state else f"{self.city} {self.zip_code}",
            self.destination_country,
        ]
        # Filter out empty or None lines
        return "<br>".join(filter(None, address_lines))

    
    @property
    def amount_value(self) -> int:
        self.amount * 100
        return self.amount*100
    
    @property
    def delivery_actual(self) -> int:
        return self.delivery_price * 16
    
    @property
    def total_actual(self) -> int:
        return self.amount + float(self.delivery_price * 16)
    
    @property
    def order_id(self):
        val = str(self.id)
        if len(val) >= 4: # more than 4 values
            return 'PO-' + val
        else:
            loopCount = 4 - len(val)
            for i in range(loopCount):
                val = '0'+ val
            return 'PO-'+ val



class Cart(models.Model):
    payment = models.OneToOneField(Payment,on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)


class CartObject(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_objects')
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    size = models.CharField(max_length=255)
  
    quantity = models.IntegerField()

    @property
    def price(self):
        return self.quantity * self.product.price
    
class DeliveryPriceByRegion(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    delivery_method = models.CharField(max_length=100, unique=True)  # Delivery method name (e.g., "Standard", "Express")
    ashanti = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    greater_accra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    volta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    western = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    eastern = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    northern = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    upper_east = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    upper_west = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bono = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bono_east = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ahafo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    savannah = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    western_north = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    oti = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    central = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery Method: {self.delivery_method}"
