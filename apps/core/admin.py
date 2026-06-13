from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import HeroSlide


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("thumbnail_preview", "page_badge", "title", "is_active", "sort_order", "created_at")
    list_display_links = ("thumbnail_preview", "title")
    list_editable = ("is_active", "sort_order")
    list_filter = ("page", "is_active")
    search_fields = ("title", "subtitle")
    fieldsets = (
        ("Page cible", {
            "fields": ("page",),
        }),
        ("Image", {
            "fields": ("image", "image_preview"),
            "classes": ("wide",),
        }),
        ("Contenu", {
            "fields": ("title", "subtitle", "cta_text", "cta_url"),
            "classes": ("wide",),
        }),
        ("Publication", {
            "fields": ("is_active", "sort_order"),
        }),
    )
    readonly_fields = ("image_preview",)
    save_on_top = True

    def thumbnail_preview(self, obj):
        if obj.pk and obj.image:
            return mark_safe(
                f'<img src="{obj.image_thumb.url}" width="100" height="56" '
                f'style="object-fit:cover; border-radius:2px; border:1px solid #c1c8c2;" />'
            )
        return "—"
    thumbnail_preview.short_description = "Aperçu"
    thumbnail_preview.allow_tags = True

    def page_badge(self, obj):
        colors = {
            "home": "primary",
            "login": "info",
            "register": "success",
            "forgot_password": "warning",
            "otp_verify": "secondary",
        }
        color = colors.get(obj.page, "secondary")
        labels = dict(HeroSlide.PAGE_CHOICES)
        label = labels.get(obj.page, obj.page)
        return mark_safe(f'<span class="badge badge-{color}">{label}</span>')
    page_badge.short_description = "Page"
    page_badge.allow_tags = True

    def image_preview(self, obj):
        if obj.pk and obj.image:
            return mark_safe(
                f'<div class="hero-preview">'
                f'<img src="{obj.image.url}" width="600" style="max-width:100%; '
                f'border-radius:4px; border:1px solid #c1c8c2; box-shadow:0 2px 8px rgba(0,0,0,0.08);" />'
                f'</div>'
            )
        return "—"
    image_preview.short_description = "Aperçu de l'image"
    image_preview.allow_tags = True
