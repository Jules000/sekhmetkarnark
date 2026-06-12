from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("webhook/tranzak/", views.tranzak_webhook, name="tranzak-webhook"),
    path("succes/", views.payment_success, name="payment-success"),
    path("annule/", views.payment_cancel, name="payment-cancel"),
]
