import ast
from django.shortcuts import render, redirect
from django.views import View
from .models import AccessRequest, Product,Cart, CartObject, Payment
from home.models import DeliveryPriceByRegion
from django.contrib.auth import login, logout, authenticate
from .deliveryRatesGen import generate_shipping_cost
from userAdmin.models import Accessible



# Create your views here.

class Home(View):
    
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/store/')
        return render(request,'home/homePage.html')
    
    def post(self,request):
        if 'requestAccess' in request.POST:
            email = request.POST.get('email')

            accessRequest = AccessRequest(email=email)

            accessRequest.save()
            print('saved')
            

            return redirect('/')

        if 'Access' in request.POST:
            password = request.POST.get('password')

            try:
                accessRequest = AccessRequest.objects.get(password=password)
            except AccessRequest.DoesNotExist:
                print('Invalid Password.')
                accessRequest = None
            
            if accessRequest:
                user = authenticate(request, username=accessRequest.username, password=password)
                if user is not None:
                    # Log the user in
                    login(request, user)
                    return redirect('/store/')  # Redirect to a home page or another page
                else:
                    print("Invalid username or password")
                    return redirect('/')
            else:
                return redirect('/')

            

class Store(View):

    def get(self,request):
        accessible = Accessible.objects.all()[0]
        if accessible.access == True:
            if request.user.is_authenticated:
                pass
            else:
                return redirect('/')
        nomaskGrey = Product.objects.get(name='NoMask Grey')
        nomaskBlack = Product.objects.get(name='NoMask Black')


        context ={
            'nomaskGrey':nomaskGrey,
            'nomaskBlack':nomaskBlack,
        }
        return render(request,'home/store.html',context)
    
class MakePayment(View):
    def get(self,request,ref):
        accessible = Accessible.objects.all()[0]
        if accessible.access == True:
            if request.user.is_authenticated:
                pass
            else:
                return redirect('/')
        payment = Payment.objects.get(ref=ref)
        ship_to = True

        if payment.destination_country != 'Ghana':
            items = {
               
                'hoodie':0,
               
            }
            for item in payment.cart.cart_objects.all():
                items['hoodie'] += item.quantity
            delivery_cost = generate_shipping_cost(items,payment.destination_country)
            print(delivery_cost)
            if 'N/A' in str(delivery_cost):
                delivery_cost = 0
                ship_to = False #
            else:
                payment.delivery_price = round(delivery_cost,2)
                payment.save()

            print(items,delivery_cost)
        else:
            delivery_price_object = DeliveryPriceByRegion.objects.all()[0]
            delivery_cost = getattr(delivery_price_object,payment.state.lower())
            payment.delivery_price =  delivery_cost/16
            payment.save()
            
        
        return render(request,'home/makePayment.html',{'payment':payment})
    
    def post(self,request,ref):
        payment = Payment.objects.get(ref=ref)
        return render(request,'home/makePayment.html',{'payment':payment})
    
class Checkout(View):
    
    def get(self,request):
        accessible = Accessible.objects.all()[0]
        if accessible.access == True:
            if request.user.is_authenticated:
                pass
            else:
                return redirect('/')
        return render(request,'home/checkout.html') 
    
    def post(self,request):
        if 'pay' in request.POST:
            cartData = request.POST.get('cartData')
            cartData =ast.literal_eval(cartData)

            

            # delivery info 
            firstName = request.POST.get('fname')
            lastName = request.POST.get('lname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            orderNotes = request.POST.get('orderNotes')
            street_address_1 = request.POST.get('street_address_1')
            street_address_2 = request.POST.get('street_address_2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip_code = request.POST.get('zip')
            destination_country = request.POST.get('destination_country')
            deliveryInfo = request.POST.get('deliveryInfo')
            cart_total = request.POST.get('cart-total')
            country_code = request.POST.get('country_code')
            pickupdata = request.POST.get('pickupdata')
            accralocation = request.POST.get('location')

            if pickupdata == 'yes':
                pickupdata = True
            else:
                pickupdata = False

            payment = Payment(first_name=firstName,last_name=lastName,email=email,country_code=country_code,phone=phone,order_notes=orderNotes,street_address_1=street_address_1,street_address_2=street_address_2,city=city,state=state,zip_code=zip_code,destination_country=destination_country,additional_info=deliveryInfo,amount=float(cart_total),pickupdata=pickupdata,accralocation=accralocation)
            print(accralocation)
            payment.save()
            
            # on payment save create cart for payment
            cart = Cart.objects.get_or_create(payment=payment) # create cart for payment
            cart[0].save()

            # loop through cart object list to append to cart
            for obj in cartData:
                print(obj['product_id'])
                product = Product.objects.get(unique_id=obj['product_id'])
                cartObj = CartObject(cart=cart[0],product=product,size=obj['selectedSize'],quantity=obj['quantity'])
                
                cartObj.save()


            return redirect(f'/makePayment/{payment.ref}/')
        
    
class Contact(View):
    def get(self,request):
        return render(request,'home/contact.html')

class About(View):
    def get(self,request):
        return render(request,'home/about.html')
    
class OrderSuccess(View):
    
    def get(self,request,ref):
        accessible = Accessible.objects.all()[0]
        if accessible.access == True:
            if request.user.is_authenticated:
                pass
            else:
                return redirect('/')
        payment = Payment.objects.get(ref=ref)
        if not payment.verified:
            for item in payment.cart.cart_objects.all():
                pass
                
        payment.verified =True
        payment.save()
        context={
            'payment':payment,
        }
        return render(request,'home/orderSuccess.html',context)