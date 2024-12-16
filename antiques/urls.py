from .views import home, contact, about, search_result, orders, view_order, view_invoice, single_antique
# from .views import AntiqueCreateView, AntiqueUpdateView, AntiqueDeleteView, AntiqueListView
from category.views import category
from django.urls import path
from . import views

urlpatterns = [
path('', home, name="home"),
path('antique/<slug:antique_slug>/', single_antique, name='single_antique'),
path('contact', contact, name="contact"),
path('about', about, name="about"),

    path('antiques/', views.antique_list, name='antique_list'),
    path('antiques/create/', views.antique_create, name='antique_create'),
    path('antiques/update/<int:pk>/', views.antique_update, name='antique_update'),
    path('antiques/delete/<int:pk>/', views.antique_delete, name='antique_delete'),

path('category/<slug:cat_slug>/', category, name="category"),
path('category/', category, name="category_list"),
path('search/', search_result, name="search_res"),
path('dashboard/orders', orders, name="orders"),
path("dashboard/view_order/<int:order_id>", view_order, name="view_order"),
path("dashboard/view_invoice/<int:invoice_id>", view_invoice, name="view_invoice"),
]