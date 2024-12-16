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
from .forms import AntiqueForm

categories_list = Category.objects.all()

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


# Fungsi untuk memeriksa apakah pengguna memiliki hak akses admin
def is_admin(user):
    return user.is_superuser or user.is_staff

# Daftar Antique
@login_required
def antique_list(request):
    if not is_admin(request.user):
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')

    antiques = Antique.objects.all().order_by('-created_on')
    return render(request, 'antiques/antique_list.html', {'antiques': antiques})

# Membuat Antique Baru
@login_required
def antique_create(request):
    if not is_admin(request.user):
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')

    if request.method == 'POST':
        form = AntiqueForm(request.POST, request.FILES)
        if form.is_valid():
            antique = form.save(commit=False)
            antique.save()
            messages.success(request, 'Antique has been created successfully!')
            return redirect('antique_list')  # Redirect ke halaman daftar
    else:
        form = AntiqueForm()

    return render(request, 'antiques/antique_form.html', {'form': form})

# Memperbarui Antique
@login_required
def antique_update(request, pk):
    if not is_admin(request.user):
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')

    antique = get_object_or_404(Antique, pk=pk)

    if request.method == 'POST':
        form = AntiqueForm(request.POST, request.FILES, instance=antique)
        if form.is_valid():
            form.save()
            messages.success(request, 'Antique has been updated successfully!')
            return redirect('antique_list')  # Redirect ke halaman daftar
    else:
        form = AntiqueForm(instance=antique)

    return render(request, 'antiques/antique_form.html', {'form': form, 'antique': antique})

# Menghapus Antique
@login_required
def antique_delete(request, pk):
    if not is_admin(request.user):
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')

    antique = get_object_or_404(Antique, pk=pk)

    if request.method == 'POST':
        antique.delete()
        messages.success(request, 'Antique has been deleted successfully!')
        return redirect('antique_list')  # Redirect ke halaman daftar

    return render(request, 'antiques/antique_confirm_delete.html', {'antique': antique})
def single_antique(request, antique_slug):
    antique = get_object_or_404(Antique, slug=antique_slug)

    related_antiques = Antique.objects.filter(
        category=antique.category
    ).exclude(id=antique.id)[:5]

    if not related_antiques.exists():
        related_antiques_message = "No related antiques available."
    else:
        related_antiques_message = None

    context = {
        'antique': antique,
        'related_antiques': related_antiques,
        'related_antiques_message': related_antiques_message,
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
    if request.user.is_authenticated:
        user = Account.objects.get(email=request.user.email)
        order_id = order.objects.all().filter(client=user).order_by('date_created')

        all_orders = Paginator(order.objects.all().filter(client=user).order_by('-date_created'), 10)
        page = request.GET.get('page')

        try:
            orders = all_orders.page(page)
        except PageNotAnInteger:
            orders = all_orders.page(1)
        except EmptyPage:
            orders = all_orders.page(all_orders.num_pages)

        context = {

            'order_id_list': orders,
        }
        return render(request, "antiques/list-orders.html", context)
    else:
        messages.error("Sorry, you need to be logged in to view your orders")
        return redirect("login")

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
