import random
import string
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from home.models import AccessRequest, Payment
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.


class UserAdmin(View):
    
    def get(self,request):
        accessRequests = AccessRequest.objects.all()
        context ={
            'accessRequests':accessRequests,
        }
        return render(request,'userAdmin/userAdmin.html',context)
    
    def post(self,request):
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

            return redirect('userAdmin')


class ManagementLogin(View):
    def get(self, request):
        return render(request, 'userAdmin/managementLogin.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:  # Check if user is a superuser
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('/userAdmin/')  # Replace with your dashboard URL name
            else:
                messages.error(request, "Access denied! Only superusers can log in.")
        else:
            messages.error(request, "Invalid username or password.")

        return render(request, 'userAdmin/managementLogin.html')


class OrdersPage(View):

    def get(self,request):
        payments = Payment.objects.all().filter(verified=True)
        context ={
            'payments':payments,
        }
        return render(request,'userAdmin/ordersPage.html',context)
    
