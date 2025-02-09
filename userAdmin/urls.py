from django.urls import path
from .views import UserAdmin, ManagementLogin, OrdersPage, OrdersDetailsPage, ContactRequests


urlpatterns =[
    path('userAdmin/',UserAdmin.as_view(),name='userAdmin'),
    path('managementLogin/',ManagementLogin.as_view(),name='managementLogin'),
    path('ordersPage/',OrdersPage.as_view(),name='ordersPage'),
    path('orderDetails/<str:ref>/',OrdersDetailsPage.as_view(),name='orderDetails'),
    path('contactRequests/',ContactRequests.as_view(),name='contactRequests'),
]