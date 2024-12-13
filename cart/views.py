from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItems
from antiques.models import Antique

def add_to_cart(request, antique_slug):
    session = request.session.session_key
    if not session:
        session = request.session.create()
        session = request.session.session_key
        cart_for_save = Cart.objects.create(cart_session=session)
        cart_for_save.save()

    try:
        session_cart = Cart.objects.get(cart_session=session)
    except ObjectDoesNotExist:
        cart_for_save = Cart.objects.create(cart_session=session)
        cart_for_save.save()
        session_cart = cart_for_save

    antique = get_object_or_404(Antique, slug=antique_slug)

    try:
        cart_item = CartItems.objects.get(cart=session_cart, antique=antique)
        cart_item.quantity += 1
        cart_item.save()
    except ObjectDoesNotExist:
        CartItems.objects.create(cart=session_cart, antique=antique, quantity=1, is_active=True)

    return redirect('cart')

def update_cart_item(request, antique_slug):
    if request.method == "POST":
        session = request.session.session_key
        user_cart = get_object_or_404(Cart, cart_session=session)
        quantity_update = int(request.POST['quantity'])

        cart_item = get_object_or_404(CartItems, cart=user_cart, antique__slug=antique_slug)
        if quantity_update != cart_item.quantity:
            cart_item.quantity = quantity_update
            cart_item.save()
    return redirect('cart')

def delete_cart_item(request, antique_slug):
    session = request.session.session_key
    user_cart = get_object_or_404(Cart, cart_session=session)
    cart_item = get_object_or_404(CartItems, cart=user_cart, antique__slug=antique_slug)
    cart_item.delete()
    return redirect('cart')

def cart(request):
    session = request.session.session_key
    user_cart = get_object_or_404(Cart, cart_session=session)
    cart_items = CartItems.objects.filter(cart=user_cart)
    total = sum(item.antique.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, "cart/cart.html", context)
