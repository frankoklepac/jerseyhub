from django.urls import path
from . import views

urlpatterns = [
    path('', views.jersey_list, name='jersey_list'),
    path('cart/', views.cart, name='cart'), 
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),  
    path('<slug:slug>/', views.jersey_detail, name='jersey_detail'),
]