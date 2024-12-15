from django.urls import path
from .views import add_to_cart, cart, delete_cart_item, update_cart_item
urlpatterns = [
    path('', cart, name='cart'),
    path('add_to_cart/<slug:antique_slug>/', add_to_cart, name="add_cart"),  # Add an antique to cart
    path('update_cart_item/<slug:antique_slug>/', update_cart_item, name="update_cart"),
    # Update an antique in the cart
    path('delete_cart_item/<slug:antique_slug>/', delete_cart_item, name="delete_cart_item"),
    # Delete an antique from the cart
]