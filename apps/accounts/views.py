from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from .models import User


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"


class CustomLogoutView(LogoutView):
    next_page = "/"


class RegisterView(CreateView):
    model = User
    template_name = "accounts/register.html"
    fields = ["first_name", "last_name", "email", "password"]
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        form.instance.username = form.instance.email
        form.instance.set_password(form.instance.password)
        return super().form_valid(form)


class ForgotPasswordView(PasswordResetView):
    template_name = "accounts/forgot_password.html"
    success_url = reverse_lazy("accounts:password_reset_done")


class OTPVerifyView(TemplateView):
    template_name = "accounts/otp_verify.html"


class DashboardView(TemplateView):
    template_name = "accounts/dashboard.html"


class OrderHistoryView(TemplateView):
    template_name = "accounts/order_history.html"


class ProfileView(TemplateView):
    template_name = "accounts/profile.html"
