from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic import ListView, DetailView
from .models import Article


@method_decorator(vary_on_headers("Accept-Language"), name="dispatch")
@method_decorator(cache_page(settings.CACHE_TTL["article_list"]), name="dispatch")
class ArticleListView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "featured_articles"
    paginate_by = 6

    def get_queryset(self):
        return (
            Article.objects.filter(status="published")
            .select_related("author", "category")
            .prefetch_related("tags")
            .only(
                "title",
                "slug",
                "excerpt",
                "featured_image",
                "reading_time",
                "published_at",
                "author__username",
                "category__name",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["secondary_articles"] = (
            Article.objects.filter(status="published")
            .select_related("author", "category")
            .order_by("-published_at")[1:4]
        )
        context["popular_articles"] = (
            Article.objects.filter(status="published")
            .order_by("-published_at")[:3]
        )
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    context_object_name = "article"
