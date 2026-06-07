from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("webhook/tranzak/", views.tranzak_webhook, name="tranzak-webhook"),
]
