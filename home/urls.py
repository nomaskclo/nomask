from django.urls import path
from .views import Home,Store, Checkout, MakePayment, Contact, About, OrderSuccess

urlpatterns =[
    path('',Home.as_view(),name='home'),
    path('store/',Store.as_view(),name='store'),
    path('checkout/',Checkout.as_view(),name='checkout'),
    path('makePayment/<str:ref>/',MakePayment.as_view(),name='makePayment'),
    path('contact/',Contact.as_view(),name='contact'),
    path('about/',About.as_view(),name='about'),
    path('orderSuccess/<str:ref>/',OrderSuccess.as_view(),name='orderSuccess')
]