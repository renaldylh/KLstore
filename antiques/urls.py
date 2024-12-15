from .views import home, contact, about, search_result, orders, view_order, view_invoice, single_antique
from .views import AntiqueCreateView, AntiqueUpdateView, AntiqueDeleteView, AntiqueListView
from category.views import category
from django.urls import path

urlpatterns = [
path('', home, name="home"),
path('antique/<slug:antique_slug>/', single_antique, name='single_antique'),
path('contact', contact, name="contact"),
path('about', about, name="about"),

    path('antiques/', AntiqueListView.as_view(), name='antique_list'),
    path('antique_create/', AntiqueCreateView.as_view(), name='antique_create'),
    path('antique_update/<int:pk>/', AntiqueUpdateView.as_view(), name='antique_update'),
    path('antique_delete/<int:pk>/', AntiqueDeleteView.as_view(), name='antique_delete'),

path('category/<slug:cat_slug>/', category, name="category"),
path('category/', category, name="category_list"),
path('search/', search_result, name="search_res"),
path('dashboard/orders', orders, name="orders"),
path("dashboard/view_order/<int:order_id>", view_order, name="view_order"),
path("dashboard/view_invoice/<int:invoice_id>", view_invoice, name="view_invoice"),
]