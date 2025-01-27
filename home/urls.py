from django.urls import path
from .views import Home,Store, Checkout, MakePayment

urlpatterns =[
    path('',Home.as_view(),name='home'),
    path('store/',Store.as_view(),name='store'),
    path('checkout/',Checkout.as_view(),name='checkout'),
    path('makePayment/<str:ref>/',MakePayment.as_view(),name='makePayment'),
]