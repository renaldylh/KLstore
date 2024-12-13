from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth, messages
from cart.models import Cart, CartItems
from .models import order, order_list, order_note_admin, invoice
from antiques.models import Antique
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
def checkout_req(request):
    special_char_list = r"!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    email_special_char_list = r"!\"#$%&'()*+,/:;<=>?@[\]^`{|}~"

    def num_checker(string):
        return any(i.isdigit() for i in string)

    def special_char_checker(string):
        for i in string:
            if i in special_char_list:
                return True
        return False

    if request.POST:
        req_user = request.user

        if req_user.is_authenticated:
            # Cek jika transaction ID sudah ada di database
            transaction_id = request.POST['transaction_id']
            invoice_exits = invoice.objects.filter(transaction_id=transaction_id).exists()

            if invoice_exits:
                messages.error(request, "Sorry, transaction ID already exists.")
                return redirect("checkout_page")

            # Menyimpan data order
            client = request.user
            order_save = order.objects.create(client=client)
            order_save.save()

            # Mengakses data keranjang
            session = request.session.session_key
            cart = Cart.objects.get(cart_session=session)
            cart_items_list = CartItems.objects.all().filter(cart=cart)
            total = 0

            for item in cart_items_list:
                # Ganti Book dengan Antique
                antique_item = Antique.objects.get(id=item.antique.id)
                price = antique_item.price
                quantity = item.quantity
                total += price * quantity

                order_list_save = order_list.objects.create(
                    order_id=order_save,
                    order_item=antique_item,
                    order_price=price,
                    order_quantity=quantity
                )
                order_list_save.save()

            # Membuat invoice
            total_price = total
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            city = request.POST['city']
            division = request.POST['division']
            zip = request.POST['zip']
            country = request.POST['country']
            order_note = request.POST['order_note']

            # Validasi input pengguna
            if num_checker(first_name):
                messages.error(request, "Sorry, First Name can't contain numbers.")
                return redirect("checkout_page")

            if special_char_checker(first_name):
                messages.error(request, "Sorry, First Name can't contain special characters.")
                return redirect("checkout_page")

            # Simpan invoice
            save_invoice = invoice.objects.create(
                order_id=order_save,
                total_price=total_price,
                first_name=first_name,
                last_name=last_name,
                address=address,
                division=division,
                city=city,
                zip=zip,
                country=country,
                transaction_id=transaction_id,
                order_note=order_note,
                transaction_method='BCA',
                invoice_status="PENDING_CHECK",
            )

            # Perbarui status order
            order.objects.filter(order_id=order_save.order_id).update(order_status="PROCESSING")

            # Hapus keranjang
            cart.delete()

            # Kurangi stok Antique
            for item in cart_items_list:
                antique_item = Antique.objects.get(id=item.antique.id)
                antique_item.stock -= item.quantity
                antique_item.save()

            messages.success(request, "Your order has been successfully received.")
            return redirect("orders")

        else:
            return redirect("login")

def checkout_page(request):
    if request.user.is_authenticated:
        return render(request, "checkout/checkout.html")
    else:
        messages.error(request, "You need to be registered to place an order.")
        return redirect("register")
