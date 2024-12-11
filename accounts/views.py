from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .forms import RegisterForm, LoginForm, ProfileEditForm, ChangePasswordForm
from .models import Account
# from cart.models import Cart
# from checkout.models import order
from datetime import datetime

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Your account has been registered. Please login now.')
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('register')
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                session_old = request.session.session_key
                session_new = request.session.session_key
                Cart.objects.filter(cart_session=session_old).update(cart_session=session_new)
                messages.success(request, "You have been logged in.")
                return redirect('dashboard')
            else:
                messages.error(request, "Email/Password don't match.")
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

@login_required(login_url='/login')
def account_home(request):
    user = request.user
    orders = order.objects.filter(client=user).order_by('-date_created')[:4]
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'order_id_list': orders,
        'total_orders': order.objects.filter(client=user).count(),
        'dilevered_orders': order.objects.filter(client=user, order_status="COMPLETED").count(),
        'registered_on': user.registered_on.strftime("%d/%m/%Y"),
        'last_login': user.last_active.strftime("%d/%m/%Y") if user.last_active else None,
    }
    return render(request, "dashboard.html", context)

@login_required(login_url='/login')
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('account_home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ProfileEditForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})

def change_pwd(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            if user.check_password(old_password):
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, "Your password has been successfully changed.")
                return redirect('login')
            else:
                messages.error(request, "Old password is incorrect.")
                return redirect('change_pwd')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ChangePasswordForm()
    return render(request, 'change_password.html', {'form': form})
