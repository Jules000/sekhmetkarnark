from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "health/",
        TemplateView.as_view(template_name="health.html", content_type="text/plain"),
        name="health",
    ),
]

urlpatterns += i18n_patterns(
    path("", include("apps.core.urls")),
    path("blog/", include("apps.blog.urls")),
    path("boutique/", include("apps.shop.urls")),
    path("panier/", include("apps.cart.urls")),
    path("commandes/", include("apps.orders.urls")),
    path("compte/", include("apps.accounts.urls")),
    path("contact/", include("apps.contact.urls")),
    path("newsletter/", include("apps.newsletter.urls")),
    path("paiements/", include("apps.payments.urls")),
    path("admin/", admin.site.urls),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns += [
            path("__debug__/", include("debug_toolbar.urls")),
        ]
