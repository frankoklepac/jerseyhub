from django.urls import path
from . import views

urlpatterns = [
    path('', views.jersey_list, name='jersey_list'),
    path('<slug:slug>/', views.jersey_detail, name='jersey_detail'),
    path('<slug:slug>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
]