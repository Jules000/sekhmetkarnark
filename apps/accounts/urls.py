from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    path("connexion/", views.CustomLoginView.as_view(), name="login"),
    path("deconnexion/", views.CustomLogoutView.as_view(), name="logout"),
    path("inscription/", views.RegisterView.as_view(), name="register"),
    path("mot-de-passe-oublie/", views.ForgotPasswordView.as_view(), name="forgot_password"),
    path("otp-verification/", views.OTPVerifyView.as_view(), name="otp_verify"),
    path("tableau-de-bord/", views.DashboardView.as_view(), name="dashboard"),
    path("commandes/", views.OrderHistoryView.as_view(), name="order_history"),
    path("profil/", views.ProfileView.as_view(), name="profile"),
]
