import random
import string
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from home.models import AccessRequest, ProductStock, Payment, DeliveryPriceByRegion, Product
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import DeliveryPriceForm, AccessibleForm, DeliveryStatusUpdateForm,ProductStockForm
from .models import Accessible
# Create your views here.


class UserAdmin(View):
    
    def get(self,request):
        if request.user.is_authenticated and request.user.is_superuser:
            pass  # Allow access
        else:
            return redirect('/')
        accessible = Accessible.objects.all()[0]
        accessRequests = AccessRequest.objects.all()
        deliveryPrices = DeliveryPriceByRegion.objects.get(name='standard')
        deliveryPricesForm = DeliveryPriceForm(instance=deliveryPrices)
        productStock = ProductStock.objects.all()[0]
        nomaskReflector = Product.objects.get(name='NoMask Reflector')
        nomaskOG = Product.objects.get(name='NoMask OG')
        accessibleForm = AccessibleForm(instance=accessible)
        productStockForm = ProductStockForm(instance=productStock)

        context ={
            'accessRequests':accessRequests,
            'deliveryPricesForm': deliveryPricesForm,
            'nomaskReflector':nomaskReflector,
            'nomaskOG':nomaskOG,
            'accessibleForm':accessibleForm,
            'productStockForm':productStockForm,
        }
        return render(request,'userAdmin/userAdmin.html',context)
    
    def post(self,request):
        nomaskReflector = Product.objects.get(name='NoMask Reflector')
        nomaskOG = Product.objects.get(name='NoMask OG')
        deliveryPrices = DeliveryPriceByRegion.objects.get(name='standard')

        if 'updateAccess' in request.POST:
            accessible = Accessible.objects.all()[0]
            form = AccessibleForm(request.POST,instance=accessible)
            if form.is_valid():
                form.save()
                return redirect('/userAdmin/')

        if 'updatePrices' in request.POST:
            form = DeliveryPriceForm(request.POST,instance=deliveryPrices)
            if form.is_valid():
                form.save()
                return redirect('/userAdmin/')
        
        if 'updateProductPrice' in  request.POST:
            currentProductPrice = int(request.POST.get('newProductPrice'))
            nomaskReflector.price = currentProductPrice
            nomaskReflector.save()
            nomaskOG.price = currentProductPrice
            nomaskOG.save()
            return redirect('/userAdmin/')
        
        if 'applyDiscount' in request.POST:
            discount = int(request.POST.get('discount_from'))
            nomaskReflector.discount_price = discount
            nomaskReflector.save()
            nomaskOG.discount_price = discount
            nomaskOG.save()
            return redirect('/userAdmin/')

        if 'updateStock' in request.POST:
            form = ProductStockForm(request.POST,instance=ProductStock.objects.all()[0])
            if form.is_valid():
                form.save()
                return redirect('/userAdmin/')

        if  'grantAccess' in request.POST:
            accessRequest = AccessRequest.objects.get(unique_id=request.POST.get('unique_id'))


            # Function to generate a unique password
            def generate_unique_password():
                characters = string.ascii_letters + string.digits + string.punctuation
                password_length = random.randint(4, 6)

                while True:
                    # Generate a random password
                    password = ''.join(random.choices(characters, k=password_length))

                    # Check if the password already exists in the database
                    if not AccessRequest.objects.filter(password=password).exists():
                        return password
                
            def generate_unique_username(email):
                base_username = email.split('@')[0]
                username = base_username
                counter = 1

                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1

                return username

            def create_user(email):
                if User.objects.filter(email=email).exists():
                    return ['exists']

                # Generate a unique password
                password = generate_unique_password()
                username = generate_unique_username(email)

                # Save the user to the database
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()

                
                return [username,password,user]


            
            accessRequestValue = create_user(accessRequest.email) 
            accessRequest.username = accessRequestValue[0]
            accessRequest.password = accessRequestValue[1]
            accessRequest.user = accessRequestValue[2]
            accessRequest.save()


            print(accessRequestValue,accessRequest.email) 

            subject = 'NoMask Password'
            text_body = f'Your Nomask Access password is {accessRequestValue[1]}'
            html_content = render_to_string('userAdmin/accessGrantedEmail.html', { 'subject': subject, 'body':text_body,})
            print(html_content)

            try:
                # Create email object with alternatives
                msg = EmailMultiAlternatives(subject, text_body, "nomaskmob@gmail.com", [accessRequest.email])
                msg.attach_alternative(html_content, "text/html")  # Attach the HTML version
                msg.send()
                print('sent')
                accessRequest.granted = True
                accessRequest.save()


                
            except Exception as e:
                print('error')
                print(f'Error sending email: {e}')  # Log the error for debugging

                return redirect('/userAdmin/')


class ManagementLogin(View):
    def get(self, request):
   
        return render(request, 'userAdmin/managementLogin.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:  # Check if user is a superuser
                login(request, user)
                print('login successfull')
                return redirect('/userAdmin/')  # Replace with your dashboard URL name
            else:
                print('Access denied! Only superusers can log in.')
        else:
            print('Invalid Username or Password')

        return render(request, 'userAdmin/managementLogin.html')


class OrdersPage(View):

    def get(self,request):
        if request.user.is_authenticated and request.user.is_superuser:
            pass  # Allow access
        else:
            return redirect('/')
        payments = Payment.objects.all().filter(verified=True)
        context ={
            'payments':payments,
        }
        return render(request,'userAdmin/ordersPage.html',context)
    

class OrdersDetailsPage(View):
    
    def get(self,request,ref):
        if request.user.is_authenticated and request.user.is_superuser:
            pass  # Allow access
        else:
            return redirect('/')
        payment = Payment.objects.get(ref=ref)
        DeliveryStatusUpdateFormCreator = DeliveryStatusUpdateForm(instance=payment)

        
        context ={
            'payment':payment,
            'DeliveryStatusUpdateFormCreator':DeliveryStatusUpdateFormCreator,
        }
        return render(request,'userAdmin/orderDetails.html',context)
    

    def post(self,request,ref):
       
        payment = Payment.objects.get(ref=ref)
         
        if 'updateDeliveryStatus' in request.POST:
            DeliveryStatusUpdateFormCreator = DeliveryStatusUpdateForm(request.POST, instance=payment)
            if DeliveryStatusUpdateFormCreator.is_valid():
                DeliveryStatusUpdateFormCreator.save()
                return redirect(f'/ordersPage/')
            else:
                print('Form errors:', DeliveryStatusUpdateFormCreator.errors) 
        
