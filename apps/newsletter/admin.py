from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "email", "is_active_badge", "is_verified_badge",
        "subscribed_at", "unsubscribed_at",
    )
    list_filter = ("is_active", "is_verified", "subscribed_at")
    search_fields = ("email",)
    readonly_fields = ("email", "verification_token",
                       "subscribed_at", "unsubscribed_at")
    save_on_top = True

    def is_active_badge(self, obj):
        if obj.is_active:
            return mark_safe('<span class="badge badge-success">Active</span>')
        return mark_safe('<span class="badge badge-danger">Désactivée</span>')
    is_active_badge.short_description = "Active"

    def is_verified_badge(self, obj):
        if obj.is_verified:
            return mark_safe('<span class="badge badge-success">Vérifié</span>')
        return mark_safe('<span class="badge badge-warning">Non vérifié</span>')
    is_verified_badge.short_description = "Vérifié"
