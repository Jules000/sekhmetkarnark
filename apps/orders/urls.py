from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("historique/", views.OrderHistoryView.as_view(), name="order_history"),
    path("facture/<int:pk>/", views.InvoiceView.as_view(), name="invoice"),
]
