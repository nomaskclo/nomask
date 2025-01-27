import ast
from django.shortcuts import render, redirect
from django.views import View
from .models import AccessRequest, Product,Cart, CartObject, Payment


# Create your views here.

class Home(View):
    
    def get(self,request):
        return render(request,'home/homePage.html')
    
    def post(self,request):
        if 'requestAccess' in request.POST:
            email = request.POST.get('email')

            accessRequest = AccessRequest(email=email)

            accessRequest.save()
            print('saved')

            return redirect('/')
class Store(View):

    def get(self,request):
        return render(request,'home/store.html')
    
class MakePayment(View):
    def get(self,request,ref):
        payment = Payment.objects.get(ref=ref)
        return render(request,'home/makePayment.html',{'payment':payment})
    
    def post(self,request,ref):
        payment = Payment.objects.get(ref=ref)
        return render(request,'home/makePayment.html',{'payment':payment})
    
class Checkout(View):
    
    def get(self,request):
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
        
    
