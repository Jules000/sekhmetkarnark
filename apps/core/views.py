from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView


@method_decorator(vary_on_headers("Accept-Language"), name="dispatch")
@method_decorator(cache_page(settings.CACHE_TTL["homepage"]), name="dispatch")
class HomePageView(TemplateView):
    template_name = "core/home.html"


class AboutPageView(TemplateView):
    template_name = "core/about.html"
