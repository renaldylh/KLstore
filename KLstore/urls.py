"""
URL configuration for KLstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from antiques.views import orders
from antiques.views import view_order
from antiques.views import view_invoice
from checkout.views import checkout_req, checkout_page
from cart.views import update_cart_item
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('antiques.urls')),
    path('cart/', include('cart.urls')),
    path('category/', include('category.urls')),
    path('checkout/', include('checkout.urls')),

    path('update_cart_item/<str:book_slug>', update_cart_item, name="update_cart"),
    # path('delete_cart_item/<str:book_slug>', delete_cart_item, name="delete_cart_item"),
    # path('search/', search_result, name="search_res"),
    path('checkout', checkout_page, name="checkout_page"),
    path('checkout_req/process', checkout_req, name="checkout_req"),
    path('dashboard/orders', orders, name="orders"),
    path("dashboard/view_order/<int:order_id>", view_order, name="view_order"),
    path("dashboard/view_invoice/<int:invoice_id>", view_invoice, name="view_invoice"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)