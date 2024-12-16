from django.urls import path
from .views import CheckoutPageView, CheckoutProcessView
from . import views

app_name = "checkout"
urlpatterns = [
    path('', CheckoutPageView.as_view(), name='checkout_page'),
    path('process/', CheckoutProcessView.as_view(), name='checkout_process'),
    path('my-orders/', views.order_list, name='order_list'),
    path('checkout/my-orders/update/<int:order_id>/', views.update_order, name='update_order'),
]