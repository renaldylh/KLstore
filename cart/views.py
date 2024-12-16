from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItems
from .forms import AddToCartForm, UpdateCartItemForm, DeleteCartItemForm

def add_to_cart(request, antique_slug):
    session = request.session.session_key or request.session.create()

    form = AddToCartForm(
        data={'antique_slug': antique_slug, 'quantity': request.POST.get('quantity', 1)},
        session=session
    )

    if form.is_valid():
        form.save()

    return redirect('cart')

def update_cart_item(request, antique_slug):
    if request.method == "POST":
        session = request.session.session_key
        form = UpdateCartItemForm(
            data={'antique_slug': antique_slug, 'quantity': request.POST['quantity']},
            session=session,
        )
        if form.is_valid():
            form.save()
    return redirect('cart')

def delete_cart_item(request, antique_slug):
    session = request.session.session_key
    form = DeleteCartItemForm(data={'antique_slug': antique_slug}, session=session)
    if form.is_valid():
        form.save()
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
