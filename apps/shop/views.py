from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic import ListView, DetailView
from .models import Product


@method_decorator(vary_on_headers("Accept-Language"), name="dispatch")
@method_decorator(cache_page(settings.CACHE_TTL["product_list"]), name="dispatch")
class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related("category").prefetch_related("images").only(
            "name", "slug", "price", "short_description", "main_image", "category__name"
        )


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
