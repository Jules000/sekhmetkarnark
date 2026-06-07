from django.conf import settings


def site_settings(request):
    return {
        "SITE_NAME": "SekhmetKarnark",
        "SITE_TAGLINE": "Sagesse Ancienne, Science Moderne",
        "SITE_TAGLINE_EN": "Ancient Wisdom, Modern Science",
        "DEBUG": settings.DEBUG,
        "CACHE_TTL": settings.CACHE_TTL,
    }
