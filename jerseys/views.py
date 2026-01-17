from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from jerseys.models import Jersey

def jersey_list(request):
    jerseys = Jersey.objects.filter(stock__gt=0)
    return render(request, 'jerseys/list.html', {'jerseys': jerseys})

def jersey_detail(request, slug):
    jersey = Jersey.objects.get(slug=slug)
    return render(request, 'jerseys/detail.html', {'jersey': jersey})

@login_required
def add_to_cart(request, slug):
    jersey = Jersey.objects.get(slug=slug)
    if jersey.stock > 0:
        cart = request.session.get('cart', [])
        cart.append({'id': jersey.id, 'name': str(jersey), 'price': float(jersey.price)})
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('jersey_detail', slug=slug) 

@login_required
def cart(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render(request, 'jerseys/cart.html', {'cart': cart, 'total': total})