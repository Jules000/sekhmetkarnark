import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TranzakTransaction

logger = logging.getLogger(__name__)


@receiver(post_save, sender=TranzakTransaction)
def on_transaction_saved(sender, instance, created, **kwargs):
    if instance.status == "success" and instance.order and not instance.order.is_paid:
        from django.utils import timezone
        instance.order.is_paid = True
        instance.order.status = "confirmed"
        instance.order.paid_at = timezone.now()
        instance.order.save(update_fields=["is_paid", "status", "paid_at"])
        logger.info("Order %s marked as paid via signal", instance.order.order_number)
