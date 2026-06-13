from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, Category, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ("image", "image_preview", "is_primary", "sort_order")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.pk and obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="80" height="80" '
                f'style="object-fit:cover; border-radius:2px;" />'
            )
        return ""
    image_preview.short_description = "Aperçu"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "product_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Produits"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail", "name", "category", "price", "compare_price",
        "stock_quantity", "is_active", "is_featured",
    )
    list_display_links = ("thumbnail", "name")
    list_editable = ("is_active", "is_featured", "stock_quantity")
    list_filter = ("is_active", "is_featured", "category")
    search_fields = ("name", "short_description", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
    save_on_top = True
    fieldsets = (
        ("Informations générales", {
            "fields": ("name", "slug", "category", "price", "compare_price", "stock_quantity"),
        }),
        ("Image principale", {
            "fields": ("main_image", "main_image_preview"),
        }),
        ("Statut", {
            "fields": ("is_active", "is_featured"),
            "classes": ("collapse",),
        }),
        ("Description", {
            "fields": ("short_description", "description"),
        }),
        ("Bénéfices & Utilisation", {
            "fields": ("benefits", "usage_instructions", "composition"),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ("main_image_preview",)

    def thumbnail(self, obj):
        if obj.main_image:
            return mark_safe(
                f'<img src="{obj.main_image_thumb.url}" width="50" height="63" '
                f'style="object-fit:cover; border-radius:2px;" />'
            )
        return "—"
    thumbnail.short_description = "Image"

    def main_image_preview(self, obj):
        if obj.pk and obj.main_image:
            return mark_safe(
                f'<img src="{obj.main_image_thumb.url}" width="200" '
                f'style="max-width:100%; border-radius:4px; border:1px solid #c1c8c2;" />'
            )
        return "—"
    main_image_preview.short_description = "Aperçu"
