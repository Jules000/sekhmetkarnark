import json
import hashlib
import hmac
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import TranzakTransaction


@csrf_exempt
@require_POST
def tranzak_webhook(request):
    payload = json.loads(request.body)
    signature = request.headers.get("X-Tranzak-Signature", "")

    expected_signature = hmac.new(
        settings.TRANZAK_WEBHOOK_SECRET.encode(),
        json.dumps(payload, separators=(",", ":")).encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        return JsonResponse({"error": "Invalid signature"}, status=400)

    transaction_id = payload.get("transactionId")
    status = payload.get("status", "failed").lower()

    TranzakTransaction.objects.update_or_create(
        tranzak_transaction_id=transaction_id,
        defaults={
            "amount": payload.get("amount", 0),
            "status": "success" if status == "success" else "failed",
            "webhook_data": payload,
        },
    )

    return JsonResponse({"status": "ok"})
