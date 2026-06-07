from django.contrib import admin
from .models import TranzakTransaction


@admin.register(TranzakTransaction)
class TranzakTransactionAdmin(admin.ModelAdmin):
    list_display = ("tranzak_transaction_id", "amount", "currency", "status", "created_at")
    list_filter = ("status", "currency")
