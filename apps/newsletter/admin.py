from django.contrib import admin
from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_verified", "subscribed_at")
    list_filter = ("is_active", "is_verified")
    search_fields = ("email",)
