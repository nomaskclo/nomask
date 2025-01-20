from django.urls import path
from .views import Home,Store

urlpatterns =[
    path('',Home.as_view(),name='home'),
    path('store/',Store.as_view(),name='store'),
]