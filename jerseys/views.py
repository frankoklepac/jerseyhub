from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction  
from urllib3 import request  
from jerseys.models import Jersey

def jersey_list(request):
    jerseys = Jersey.objects.filter(stock__gt=0)
    return render(request, 'jerseys/list.html', {'jerseys': jerseys})

def jersey_detail(request, slug):
    jersey = get_object_or_404(Jersey, slug=slug)
    return render(request, 'jerseys/detail.html', {'jersey': jersey})

@login_required
def add_to_cart(request, slug):
    jersey = get_object_or_404(Jersey, slug=slug)
    if jersey.stock <= 0:
        return redirect('jersey_detail', slug=slug)
    
    cart = request.session.get('cart', [])
    quantity = int(request.POST.get('quantity', 1))
    jersey_id = jersey.id
    if quantity < 1:
            quantity = 1  


    existing_item = next((item for item in cart if item['id'] == jersey_id), None)
    added_qty = 0
    if existing_item:
        existing_qty = existing_item.get('quantity', 1)
        new_qty = existing_qty + quantity
        if new_qty <= jersey.stock:
            existing_item['quantity'] = new_qty
            added_qty = quantity
        else:
            added_qty = jersey.stock - existing_qty
            if added_qty > 0:
                existing_item['quantity'] = jersey.stock 
            else:
                return redirect('jersey_detail', slug=slug)
    else:
        if quantity <= jersey.stock:
            cart.append({
                'id': jersey_id,
                'name': str(jersey),
                'price': float(jersey.price),
                'quantity': quantity,
                'image': jersey.image.url if jersey.image else None
            })
            added_qty = quantity
        else:
            cart.append({
                'id': jersey_id,
                'name': str(jersey),
                'price': float(jersey.price),
                'quantity': jersey.stock,
                'image': jersey.image.url if jersey.image else None
            })
            added_qty = jersey.stock
    jersey.stock -= added_qty
    jersey.save()

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('jersey_detail', slug=slug)

@login_required
def cart(request):
    cart = request.session.get('cart', [])
    fixed_cart = []
    for item in cart:
        item_copy = item.copy()  #
        item_copy['quantity'] = item_copy.get('quantity', 1)
        fixed_cart.append(item_copy)
    cart = fixed_cart 
    
    total = sum(item['price'] * item['quantity'] for item in cart)  
    return render(request, 'jerseys/cart.html', {'cart': cart, 'total': total})

@require_POST
@login_required
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', [])
    item_to_remove = next((item for item in cart if item['id'] == int(item_id)), None)
    
    if item_to_remove:
        jersey = get_object_or_404(Jersey, id=item_to_remove['id'])
        quantity_removed = item_to_remove.get('quantity', 1)  
        jersey.stock += quantity_removed
        jersey.save()
    
    cart = [item for item in cart if item['id'] != int(item_id)]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

@login_required
def clear_cart(request):
    request.session['cart'] = []
    request.session.modified = True
    return redirect('cart')

@login_required
@transaction.atomic  
def checkout(request):
    cart = request.session.get('cart', [])
    if not cart:
        return redirect('cart')
    
    total = sum(item['price'] * item.get('quantity', 1) for item in cart)
    deducted_qty_total = 0  
    
    for item in cart:
        jersey = get_object_or_404(Jersey, id=item['id'])
        qty = item.get('quantity', 1)
        if jersey.stock >= qty:
            jersey.stock -= qty
            jersey.save()
            deducted_qty_total += qty
        else:
            return redirect('cart')
    
    request.session['cart'] = []
    request.session.modified = True
    
    return render(request, 'jerseys/checkout.html', {'total': total})