from django import forms
from django.core.exceptions import ValidationError
from .models import Cart, CartItems
from antiques.models import Antique
from django.core.exceptions import ObjectDoesNotExist

class AddToCartForm(forms.Form):
    antique_slug = forms.CharField()
    quantity = forms.IntegerField(min_value=1, required=False)  # Quantity bisa kosong tapi akan diatur default-nya

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)  # Ambil session dari parameter
        super().__init__(*args, **kwargs)

    def clean_antique_slug(self):
        slug = self.cleaned_data.get('antique_slug')
        if not Antique.objects.filter(slug=slug).exists():
            raise forms.ValidationError("The antique item does not exist.")
        return slug

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        return quantity if quantity else 1  # Atur default quantity ke 1 jika kosong

    def save(self):
        antique = Antique.objects.get(slug=self.cleaned_data['antique_slug'])
        cart, _ = Cart.objects.get_or_create(cart_session=self.session)

        try:
            # Cek apakah item sudah ada di keranjang
            cart_item = CartItems.objects.get(cart=cart, antique=antique)
            cart_item.quantity += self.cleaned_data['quantity']
            cart_item.save()
        except ObjectDoesNotExist:
            # Buat item baru di keranjang jika belum ada
            CartItems.objects.create(
                cart=cart,
                antique=antique,
                quantity=self.cleaned_data['quantity'],
                is_active=True
            )

class UpdateCartItemForm(forms.Form):
    antique_slug = forms.SlugField()
    quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        super().__init__(*args, **kwargs)

    def clean_antique_slug(self):
        antique_slug = self.cleaned_data.get('antique_slug')
        if not Antique.objects.filter(slug=antique_slug).exists():
            raise ValidationError("Antique item does not exist.")
        return antique_slug

    def save(self):
        if not self.session:
            raise ValueError("Session is required.")

        antique_slug = self.cleaned_data['antique_slug']
        quantity = self.cleaned_data['quantity']

        session_cart = Cart.objects.get(cart_session=self.session)
        cart_item = CartItems.objects.get(cart=session_cart, antique__slug=antique_slug)
        cart_item.quantity = quantity
        cart_item.save()


class DeleteCartItemForm(forms.Form):
    antique_slug = forms.SlugField()

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        super().__init__(*args, **kwargs)

    def clean_antique_slug(self):
        antique_slug = self.cleaned_data.get('antique_slug')
        if not Antique.objects.filter(slug=antique_slug).exists():
            raise ValidationError("Antique item does not exist.")
        return antique_slug

    def save(self):
        if not self.session:
            raise ValueError("Session is required.")

        antique_slug = self.cleaned_data['antique_slug']
        session_cart = Cart.objects.get(cart_session=self.session)
        cart_item = CartItems.objects.get(cart=session_cart, antique__slug=antique_slug)
        cart_item.delete()
