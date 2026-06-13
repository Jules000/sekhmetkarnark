from django.conf import settings
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic import ListView, DetailView
from .models import Article, Category, Tag


@method_decorator(vary_on_headers("Accept-Language"), name="dispatch")
class ArticleListView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "featured_articles"
    paginate_by = 6

    def get_queryset(self):
        qs = (
            Article.objects.filter(status="published")
            .select_related("author", "category")
            .prefetch_related("tags")
        )
        category = self.request.GET.get("category")
        if category:
            qs = qs.filter(category__slug=category)

        tag = self.request.GET.get("tag")
        if tag:
            qs = qs.filter(tags__slug=tag)

        sort = self.request.GET.get("sort", "recent")
        if sort == "reading_time":
            qs = qs.order_by("reading_time", "-published_at")
        else:
            qs = qs.order_by("-published_at")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get("page")
        qs = Article.objects.filter(status="published")
        context["secondary_articles"] = (
            qs.select_related("author", "category")
            .order_by("-published_at")[1:4]
        )
        context["popular_articles"] = (
            qs.order_by("-published_at")[:3]
        )
        context["categories_blog"] = Category.objects.annotate(article_count=Count("article"))
        context["tags_blog"] = Tag.objects.all()
        context["current_category"] = self.request.GET.get("category", "")
        context["current_tag"] = self.request.GET.get("tag", "")
        context["current_sort"] = self.request.GET.get("sort", "recent")
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_articles"] = Article.objects.filter(
            status="published", category=self.object.category
        ).exclude(pk=self.object.pk)[:3]
        return context
