from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "price", "quantity")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number", "customer", "total", "status_badge",
        "is_paid_badge", "payment_method", "created_at",
    )
    list_filter = ("status", "is_paid", "payment_method", "created_at")
    search_fields = ("order_number", "email", "first_name", "last_name")
    inlines = [OrderItemInline]
    readonly_fields = (
        "order_number", "total", "shipping_cost", "created_at", "updated_at",
    )
    save_on_top = True
    fieldsets = (
        ("Commande", {
            "fields": ("order_number", "status", "is_paid", "paid_at", "payment_method"),
        }),
        ("Client", {
            "fields": (
                "first_name", "last_name", "email", "phone",
            ),
        }),
        ("Adresse de livraison", {
            "fields": (
                "address_line_1", "address_line_2", "city",
                "postal_code", "country",
            ),
        }),
        ("Totaux", {
            "fields": ("total", "shipping_cost"),
            "classes": ("collapse",),
        }),
        ("Notes", {
            "fields": ("notes",),
            "classes": ("collapse",),
        }),
        ("Dates", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    def customer(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer.short_description = "Client"

    def status_badge(self, obj):
        colors = {
            "pending": "warning",
            "confirmed": "info",
            "shipped": "primary",
            "delivered": "success",
            "cancelled": "danger",
        }
        color = colors.get(obj.status, "secondary")
        labels = {
            "pending": "En attente",
            "confirmed": "Confirmée",
            "shipped": "Expédiée",
            "delivered": "Livrée",
            "cancelled": "Annulée",
        }
        label = labels.get(obj.status, obj.status)
        return mark_safe(f'<span class="badge badge-{color}">{label}</span>')
    status_badge.short_description = "Statut"

    def is_paid_badge(self, obj):
        if obj.is_paid:
            return mark_safe('<span class="badge badge-success">Payée</span>')
        return mark_safe('<span class="badge badge-warning">Impayée</span>')
    is_paid_badge.short_description = "Paiement"
