from checkout.models import order
from datetime import datetime
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView
from .forms import RegisterForm, LoginForm, ProfileEditForm, ChangePasswordForm
from cart.models import Cart

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, 'Your account has been registered. Please login now.')
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return redirect('register')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(self.request, user)
            session_old = self.request.session.session_key
            session_new = self.request.session.session_key
            Cart.objects.filter(cart_session=session_old).update(cart_session=session_new)
            messages.success(self.request, "You have been logged in.")
            return redirect('dashboard')
        else:
            messages.error(self.request, "Email/Password don't match.")
            return redirect('login')

    def form_invalid(self, form):
        messages.error(self.request, "Invalid login credentials.")
        return redirect('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class LogoutView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('login')


class ProfileEditView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = 'accounts/edit_profile.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('profile_edit')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return redirect('profile_edit')


class ChangePasswordView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    template_name = 'accounts/change_password.html'
    form_class = ChangePasswordForm

    def form_valid(self, form):
        user = self.request.user
        old_password = form.cleaned_data['old_password']
        if user.check_password(old_password):
            user.set_password(form.cleaned_data['password'])
            user.save()
            update_session_auth_hash(self.request, user)
            messages.success(self.request, "Your password has been successfully changed.")
            return redirect('login')
        else:
            messages.error(self.request, "Old password is incorrect.")
            return redirect('change_password')

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return redirect('change_password')

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
    return render(request, "accounts/dashboard.html", context)
