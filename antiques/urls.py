from .views import home, contact, about, search_result, orders, view_order, view_invoice, single_antique
from category.views import category
from django.urls import path


urlpatterns = [
path('', home, name="home"),
path('contact', contact, name="contact"),
path('about', about, name="about"),
path('category/<slug:cat_slug>/', category, name="category"),
path('category/', category, name="category_list"),
path('antique/<slug:single_antique_slug>', single_antique, name="single_antique"),
path('search/', search_result, name="search_res"),
path('orders', orders, name="orders"),
path('view_order/<int:order_id>', view_order, name="view_order"),
path('view_invoice/<int:invoice_id>', view_invoice, name="view_invoice"),
]