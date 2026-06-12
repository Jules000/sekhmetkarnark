import json
import hashlib
import hmac
import logging

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import TranzakTransaction
from .services import TranzakClient, TranzakError

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def tranzak_webhook(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    signature = request.headers.get("X-Tranzak-Signature", "")
    expected_signature = hmac.new(
        settings.TRANZAK_WEBHOOK_SECRET.encode(),
        json.dumps(payload, separators=(",", ":")).encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        return JsonResponse({"error": "Invalid signature"}, status=400)

    transaction_id = payload.get("transactionId")
    if not transaction_id:
        return JsonResponse({"error": "Missing transactionId"}, status=400)

    raw_status = payload.get("status", "").lower()
    if raw_status == "success":
        mapped_status = "success"
    elif raw_status == "pending":
        mapped_status = "pending"
    else:
        mapped_status = "failed"

    reference = payload.get("reference", "")

    tran, created = TranzakTransaction.objects.update_or_create(
        tranzak_transaction_id=transaction_id,
        defaults={
            "amount": payload.get("amount", 0),
            "currency": payload.get("currency", "XAF"),
            "status": mapped_status,
            "webhook_data": payload,
        },
    )

    if mapped_status == "success" and reference:
        from apps.orders.models import Order
        try:
            order = Order.objects.get(order_number=reference)
            tran.order = order
            tran.save(update_fields=["order"])
            if not order.is_paid:
                order.is_paid = True
                order.status = "confirmed"
                order.paid_at = timezone.now()
                order.save(update_fields=["is_paid", "status", "paid_at"])
                logger.info("Order %s marked as paid via webhook", order.order_number)
        except Order.DoesNotExist:
            logger.warning("Order %s not found for webhook transaction %s", reference, transaction_id)

    return JsonResponse({"status": "ok"})


def payment_success(request):
    transaction_id = request.GET.get("transactionId")
    reference = request.GET.get("reference", "")
    status = "success"

    if transaction_id:
        try:
            tran = TranzakTransaction.objects.get(tranzak_transaction_id=transaction_id)
            status = tran.status
        except TranzakTransaction.DoesNotExist:
            try:
                data = TranzakClient().get_transaction_status(transaction_id)
                raw_status = data.get("status", "").lower()
                status = "success" if raw_status == "success" else "failed"
                TranzakTransaction.objects.update_or_create(
                    tranzak_transaction_id=transaction_id,
                    defaults={
                        "amount": data.get("amount", 0),
                        "currency": data.get("currency", "XAF"),
                        "status": status,
                        "webhook_data": data,
                    },
                )
            except TranzakError:
                pass

        if status == "success" and reference:
            from apps.orders.models import Order
            try:
                order = Order.objects.get(order_number=reference)
                if not order.is_paid:
                    order.is_paid = True
                    order.status = "confirmed"
                    order.paid_at = timezone.now()
                    order.save(update_fields=["is_paid", "status", "paid_at"])
            except Order.DoesNotExist:
                pass

    return render(request, "payments/result.html", {
        "status": status,
        "reference": reference,
    })


def payment_cancel(request):
    reference = request.GET.get("reference", "")
    return render(request, "payments/result.html", {
        "status": "cancelled",
        "reference": reference,
    })
