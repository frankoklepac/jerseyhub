from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction  
from urllib3 import request  
from jerseys.models import Jersey, Team

def jersey_list(request):
    jerseys = Jersey.objects.all()
    teams = Team.objects.all()
    
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        jerseys = jerseys.filter(price__gte=price_min)
    if price_max:
        jerseys = jerseys.filter(price__lte=price_max)
    
    team_id = request.GET.get('team')
    if team_id:
        jerseys = jerseys.filter(team_id=team_id)
    
    brand = request.GET.get('brand')
    if brand:
        jerseys = jerseys.filter(brand=brand)
    
    jersey_type = request.GET.get('type')
    if jersey_type:
        jerseys = jerseys.filter(type=jersey_type)
    
    size = request.GET.get('size')
    if size:
        jerseys = jerseys.filter(size=size)
    
    if request.GET.get('is_retro'):
        jerseys = jerseys.filter(is_retro=True)
    
    context = {
        'jerseys': jerseys,
        'teams': teams,
    }
    return render(request, 'jerseys/list.html', context)

def jersey_detail(request, slug):
    jersey = get_object_or_404(Jersey, slug=slug)
    return render(request, 'jerseys/detail.html', {'jersey': jersey})

@login_required
def add_to_cart(request, slug):
    jersey = get_object_or_404(Jersey, slug=slug)
    if jersey.stock <= 0:
        messages.error(request, 'This jersey is out of stock!')
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
                messages.warning(request, 'Cannot add more—stock limit reached!')
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
        
        messages.info(request, f'Removed {quantity_removed} x {item_to_remove["name"]} from cart. Stock updated.')
    else:
        messages.warning(request, 'Item not found in cart.')
    
    cart = [item for item in cart if item['id'] != int(item_id)]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

@login_required
def clear_cart(request):
    cart = request.session.get('cart', [])
    
    for item in cart:
        try:
            jersey = get_object_or_404(Jersey, id=item['id'])
            jersey.stock += item.get('quantity', 1)
            jersey.save()
        except Jersey.DoesNotExist:
            messages.warning(request, f"Could not find jersey with ID {item['id']} to update stock.")

    request.session['cart'] = []
    request.session.modified = True
    messages.info(request, 'Cart cleared and stock restored!')
    return redirect('cart')

@login_required
@transaction.atomic  
def checkout(request):
    cart = request.session.get('cart', [])
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    total = sum(item['price'] * item.get('quantity', 1) for item in cart)
    
    request.session['cart'] = []
    request.session.modified = True
    
    messages.success(request, f'Order placed successfully! Total: ${total:.2f}.')
    return render(request, 'jerseys/checkout.html', {'total': total})