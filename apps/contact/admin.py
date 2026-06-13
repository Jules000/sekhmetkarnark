from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name", "email", "subject", "is_read_badge", "created_at",
    )
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")
    save_on_top = True
    fieldsets = (
        ("Expéditeur", {
            "fields": ("name", "email"),
        }),
        ("Message", {
            "fields": ("subject", "message"),
        }),
        ("Traitement", {
            "fields": ("is_read", "created_at"),
        }),
    )

    def is_read_badge(self, obj):
        if obj.is_read:
            return mark_safe('<span class="badge badge-success">Lu</span>')
        return mark_safe('<span class="badge badge-warning">Non lu</span>')
    is_read_badge.short_description = "Statut"

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Marquer comme lu"

    actions = ["mark_as_read"]
