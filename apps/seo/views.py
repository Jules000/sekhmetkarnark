from django.http import HttpResponse
from django.views.generic import TemplateView


class RobotsView(TemplateView):
    template_name = "seo/robots.txt"
    content_type = "text/plain"


class SitemapView(TemplateView):
    template_name = "seo/sitemap.xml"
    content_type = "application/xml"
