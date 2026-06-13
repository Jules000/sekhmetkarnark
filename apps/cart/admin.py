from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("product", "quantity", "created_at")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "session_key", "item_count", "created_at")
    search_fields = ("user__email", "user__username", "session_key")
    inlines = [CartItemInline]
    readonly_fields = ("user", "session_key", "created_at", "updated_at")

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Articles"
