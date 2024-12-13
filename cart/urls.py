from django.urls import path
from .views import add_to_cart, cart, delete_cart_item, update_cart_item
from antiques.views import view_order,view_invoice
urlpatterns = [
    path('', cart, name='cart'),
    path('add_to_cart/<str:user_book>', add_to_cart, name="add_cart"),
    path('update_cart_item/<str:book_slug>', update_cart_item, name="update_cart"),
    path('delete_cart_item/<str:book_slug>', delete_cart_item, name="delete_cart_item"),
]