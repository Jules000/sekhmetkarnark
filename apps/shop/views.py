from django.conf import settings
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic import ListView, DetailView
from .models import Product, Category


@method_decorator(vary_on_headers("Accept-Language"), name="dispatch")
class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related("category").prefetch_related("images")

        category = self.request.GET.get("category")
        if category:
            qs = qs.filter(category__slug=category)

        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(short_description__icontains=q))

        price_min = self.request.GET.get("price_min")
        if price_min:
            qs = qs.filter(price__gte=price_min)
        price_max = self.request.GET.get("price_max")
        if price_max:
            qs = qs.filter(price__lte=price_max)

        in_stock = self.request.GET.get("in_stock")
        if in_stock:
            qs = qs.filter(stock_quantity__gt=0)

        sort = self.request.GET.get("sort", "newest")
        if sort == "price_asc":
            qs = qs.order_by("price")
        elif sort == "price_desc":
            qs = qs.order_by("-price")
        elif sort == "name":
            qs = qs.order_by("name")
        else:
            qs = qs.order_by("-created_at")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = (
            Category.objects.annotate(product_count=Count("products"))
            .filter(product_count__gt=0)
            .order_by("name")
        )
        context["current_category"] = self.request.GET.get("category", "")
        context["current_sort"] = self.request.GET.get("sort", "newest")
        context["current_q"] = self.request.GET.get("q", "")
        context["current_price_min"] = self.request.GET.get("price_min", "")
        context["current_price_max"] = self.request.GET.get("price_max", "")
        context["current_in_stock"] = self.request.GET.get("in_stock", "")
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_products"] = Product.objects.filter(
            category=self.object.category, is_active=True
        ).exclude(pk=self.object.pk)[:3]
        return context
