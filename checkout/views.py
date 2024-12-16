from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from checkout.forms import CheckoutForm, OrderUpdateForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import order
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class CheckoutPageView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        form = CheckoutForm()
        return render(request, "checkout/checkout.html", {'form': form})

class CheckoutProcessView(LoginRequiredMixin, View):
    login_url = '/login'

    def post(self, request):
        form = CheckoutForm(request.POST)
        session_key = request.session.session_key

        if not session_key:
            messages.error(request, "Session expired. Please try again.")
            return redirect("checkout:checkout_page")

        if form.is_valid():
            try:
                form.process_checkout(request.user, session_key)
                messages.success(request, "Your order has been successfully received.")
                return redirect("orders")
            except Exception as e:
                messages.error(request, f"Error processing checkout: {str(e)}")
                return redirect("checkout:checkout_page")
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect("checkout:checkout_page")

@login_required
def order_list(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')

    # Fetch all orders, ordered by date created
    orders = order.objects.all().order_by('-date_created')

    # Set up pagination
    paginator = Paginator(orders, 10)  # 10 orders per page
    page = request.GET.get('page')

    try:
        paginated_orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        paginated_orders = paginator.page(paginator.num_pages)

    context = {
        'orders': paginated_orders,
    }

    return render(request, 'checkout/ order_list.html', context)
@login_required
def update_order(request, order_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('home')

    order_instance = get_object_or_404(order, pk=order_id)

    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order has been updated successfully.')
            return redirect('checkout:order_list')  # Ensure correct URL name
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = OrderUpdateForm(instance=order_instance)

    return render(request, 'checkout/update_order.html', {'form': form, 'order': order_instance})