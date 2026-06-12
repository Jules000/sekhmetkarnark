import logging

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, TemplateView, View

from apps.cart.models import Cart
from apps.payments.services import TranzakClient, TranzakError

from .models import Order, OrderItem

logger = logging.getLogger(__name__)


def _get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


class CheckoutView(TemplateView):
    template_name = "orders/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = _get_cart(self.request)
        cart_items = cart.items.all().select_related("product") if cart else []
        total = sum(item.product.price * item.quantity for item in cart_items) if cart_items else 0
        context["cart_items"] = cart_items
        context["cart_total"] = total
        context["tranzak_public_key"] = settings.TRANZAK_APP_ID
        context["tranzak_mode"] = settings.TRANZAK_MODE
        return context

    def post(self, request, *args, **kwargs):
        cart = _get_cart(request)
        cart_items = cart.items.all().select_related("product")

        if not cart_items:
            messages.error(request, "Votre panier est vide.")
            return redirect("cart:cart_detail")

        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        postal_code = request.POST.get("postal_code", "").strip()

        if not all([first_name, last_name, email, address, city, postal_code]):
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, self.template_name, self.get_context_data())

        total = sum(item.product.price * item.quantity for item in cart_items)

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order_number=self._generate_order_number(),
            first_name=first_name,
            last_name=last_name,
            email=email,
            address_line_1=address,
            city=city,
            postal_code=postal_code,
            total=total,
            payment_method="tranzak",
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
            )

        cart.items.all().delete()

        try:
            success_url = request.build_absolute_uri(
                reverse("payments:payment-success") + f"?reference={order.order_number}"
            )
            cancel_url = request.build_absolute_uri(
                reverse("payments:payment-cancel") + f"?reference={order.order_number}"
            )

            client = TranzakClient()
            result = client.create_checkout(
                amount=float(total),
                currency="XAF",
                reference=order.order_number,
                success_url=success_url,
                cancel_url=cancel_url,
                description=f"Commande {order.order_number}",
            )

            checkout_url = result.get("checkoutUrl") or result.get("paymentUrl") or result.get("url")
            if checkout_url:
                return redirect(checkout_url)
            else:
                logger.error("Tranzak returned no checkout URL: %s", result)
                messages.error(request, "Impossible d'initier le paiement. Veuillez réessayer.")
                return redirect("orders:checkout")

        except TranzakError as e:
            logger.error("Payment initiation failed for order %s: %s", order.order_number, e)
            messages.error(request, "Le service de paiement est temporairement indisponible.")
            return redirect("orders:checkout")

    @staticmethod
    def _generate_order_number():
        from django.utils.crypto import get_random_string
        import time
        ts = int(time.time() * 1000) % 100000
        rand = get_random_string(4, "ABCDEFGHJKLMNPQRSTUVWXYZ23456789")
        return f"SK-{ts}-{rand}"


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
