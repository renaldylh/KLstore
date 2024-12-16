from django import forms
from django.core.exceptions import ValidationError
from .models import invoice, order, order_list
from cart.models import Cart,CartItems
from antiques.models import Antique

class CheckoutForm(forms.Form):
    transaction_id = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=70, required=True)
    last_name = forms.CharField(max_length=70, required=True)
    address = forms.CharField(max_length=500, required=True)
    city = forms.CharField(max_length=100, required=True)
    division = forms.CharField(max_length=60, required=True)
    zip = forms.CharField(max_length=60, required=True)
    country = forms.CharField(max_length=100, required=False)
    order_note = forms.CharField(max_length=500, required=False)

    def clean_transaction_id(self):
        transaction_id = self.cleaned_data['transaction_id']
        if invoice.objects.filter(transaction_id=transaction_id).exists():
            raise ValidationError("Sorry, transaction ID already exists.")
        return transaction_id

    def clean_first_name(self):
        special_char_list = r"!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        first_name = self.cleaned_data['first_name']

        if any(char.isdigit() for char in first_name):
            raise ValidationError("Sorry, First Name can't contain numbers.")

        if any(char in special_char_list for char in first_name):
            raise ValidationError("Sorry, First Name can't contain special characters.")

        return first_name

    def process_checkout(self, user, session):
        cart = Cart.objects.get(cart_session=session)
        cart_items_list = CartItems.objects.filter(cart=cart)

        total = 0
        for item in cart_items_list:
            antique_item = Antique.objects.get(id=item.antique.id)
            total += antique_item.price * item.quantity

        # Create order
        order_save = order.objects.create(client=user)

        for item in cart_items_list:
            antique_item = Antique.objects.get(id=item.antique.id)
            order_list.objects.create(
                order_id=order_save,
                order_item=antique_item,
                order_price=antique_item.price,
                order_quantity=item.quantity
            )
            antique_item.stocks -= item.quantity
            antique_item.save()

        # Create invoice
        invoice.objects.create(
            order_id=order_save,
            total_price=total,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            address=self.cleaned_data['address'],
            city=self.cleaned_data['city'],
            division=self.cleaned_data['division'],
            zip=self.cleaned_data['zip'],
            country=self.cleaned_data.get('country', ''),
            transaction_id=self.cleaned_data['transaction_id'],
            order_note=self.cleaned_data.get('order_note', ''),
            transaction_method='BCA',
            invoice_status="PENDING_CHECK",
        )

        order_save.order_status = "PROCESSING"
        order_save.save()
        cart.delete()

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = order
        fields = ['order_status']
        widgets = {
            'order_status': forms.Select(attrs={'class': 'form-control'}),
        }

