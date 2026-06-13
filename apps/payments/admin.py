from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import TranzakTransaction


@admin.register(TranzakTransaction)
class TranzakTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "tranzak_transaction_id", "order_link", "amount",
        "currency", "status_badge", "created_at",
    )
    list_filter = ("status", "currency", "created_at")
    search_fields = ("tranzak_transaction_id",)
    readonly_fields = ("tranzak_transaction_id", "amount", "currency",
                       "status", "webhook_data", "created_at", "updated_at")
    save_on_top = True

    def order_link(self, obj):
        if obj.order:
            from django.urls import reverse
            url = reverse("admin:orders_order_change", args=[obj.order.pk])
            return mark_safe(f'<a href="{url}">{obj.order.order_number}</a>')
        return "—"
    order_link.short_description = "Commande"

    def status_badge(self, obj):
        colors = {
            "pending": "warning",
            "success": "success",
            "failed": "danger",
        }
        color = colors.get(obj.status, "secondary")
        return mark_safe(f'<span class="badge badge-{color}">{obj.status}</span>')
    status_badge.short_description = "Statut"
