# checkout/urls.py
from django.urls import path
from .views import checkout_req, checkout_page

urlpatterns = [
    path('', checkout_page, name="checkout_page"),
    path('process/', checkout_req, name="checkout_req"),
]
