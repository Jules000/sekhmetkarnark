from django.views.generic import TemplateView, ListView
from .models import Order


class CheckoutView(TemplateView):
    template_name = "orders/checkout.html"


class OrderHistoryView(ListView):
    model = Order
    template_name = "orders/order_history.html"
    context_object_name = "orders"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        return Order.objects.none()


class InvoiceView(TemplateView):
    template_name = "orders/invoice.html"
