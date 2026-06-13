from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Article, Category, Tag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail", "title", "status", "category", "author",
        "published_at", "reading_time",
    )
    list_display_links = ("thumbnail", "title")
    list_filter = ("status", "category", "tags")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    save_on_top = True
    fieldsets = (
        ("Informations générales", {
            "fields": ("title", "slug", "author", "category", "tags"),
        }),
        ("Image mise en avant", {
            "fields": ("featured_image", "featured_image_preview"),
            "description": "Cette image s'affichera sur la page listant tous les articles du blog.",
        }),
        ("Contenu", {
            "fields": ("excerpt", "content"),
        }),
        ("Publication", {
            "fields": ("status", "published_at", "reading_time"),
        }),
    )
    readonly_fields = ("featured_image_preview",)

    def thumbnail(self, obj):
        if obj.featured_image:
            return mark_safe(
                f'<img src="{obj.featured_image_thumb.url}" width="80" height="45" '
                f'style="object-fit:cover; border-radius:2px;" />'
            )
        return "—"
    thumbnail.short_description = "Image"

    def featured_image_preview(self, obj):
        if obj.pk and obj.featured_image:
            return mark_safe(
                f'<img src="{obj.featured_image_thumb.url}" width="400" '
                f'style="max-width:100%; border-radius:4px; border:1px solid #c1c8c2;" />'
            )
        return "—"
    featured_image_preview.short_description = "Aperçu"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "article_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = "Articles"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "article_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = "Articles"
