from category.models import Category
from checkout.models import order_list
from checkout.models import order
from accounts.models  import Account
from checkout.models import invoice
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Antique, Category

def home(request):
    antiques_list = Antique.objects.all().order_by('-created_on')
    paginator = Paginator(antiques_list, 10)
    page = request.GET.get('page')

    try:
        antiques = paginator.page(page)
    except PageNotAnInteger:
        antiques = paginator.page(1)
    except EmptyPage:
        antiques = paginator.page(paginator.num_pages)

    context = {
        'antiques': antiques,
    }
    return render(request, 'antiques/index.html', context)


def contact(request):

    return render(request, 'antiques/contact-us.html')

def about(request):

    return render(request, 'antiques/about.html')

def single_antique(request, antique_slug):
    antique = get_object_or_404(Antique, slug=antique_slug)
    related_antiques = Antique.objects.filter(category=antique.category).exclude(id=antique.id)[:5]

    context = {
        'antique': antique,
        'related_antiques': related_antiques,
    }
    return render(request, 'antiques/antique-single-page.html', context)

def search_result(request):
    query = request.GET.get('query', '')
    antiques = Antique.objects.filter(title__icontains=query) if query else []

    context = {
        'antiques': antiques,
        'query': query,
    }
    return render(request, 'antiques/search_res.html', context)

# def antiques_by_category(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     antiques_list = Antique.objects.filter(category=category).order_by('-created_on')
#     paginator = Paginator(antiques_list, 10)
#     page = request.GET.get('page')
#
#     try:
#         antiques = paginator.page(page)
#     except PageNotAnInteger:
#         antiques = paginator.page(1)
#     except EmptyPage:
#         antiques = paginator.page(paginator.num_pages)
#
#     context = {
#         'category': category,
#         'antiques': antiques,
#     }
#     return render(request, 'antiques-by-category.html', context)

@login_required(login_url='/login')
def orders(request):
    user = request.user
    orders = Antique.objects.filter(stocks_available=True).order_by('-modified_on')

    paginator = Paginator(orders, 10)
    page = request.GET.get('page')

    try:
        paginated_orders = paginator.page(page)
    except PageNotAnInteger:
        paginated_orders = paginator.page(1)
    except EmptyPage:
        paginated_orders = paginator.page(paginator.num_pages)

    context = {
        'orders': paginated_orders,
    }
    return render(request, 'antiques/list-orders.html', context)

@login_required(login_url='/login')
def view_order(request, order_id):
    order_items = order_list.objects.filter(order_id=order_id)
    invoice_details = invoice.objects.filter(order_id=order_id)

    context = {
        'order_id': order_id,
        'order_items_list': order_items,
        'invoice_list': invoice_details,
    }
    return render(request, 'antiques/view_order.html', context)

@login_required(login_url='/login')
def view_invoice(request, invoice_id):
    invoice_data = get_object_or_404(invoice, invoice_id=invoice_id)

    context = {
        'invoice': invoice_data,
    }
    return render(request, 'antiques/view_invoice.html', context)
