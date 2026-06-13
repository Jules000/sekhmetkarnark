from django.conf import settings
from .models import HeroSlide


def site_settings(request):
    hero_slides = HeroSlide.objects.filter(is_active=True, page="home")[:5]
    hero_login = HeroSlide.objects.filter(is_active=True, page="login").first()
    hero_register = HeroSlide.objects.filter(is_active=True, page="register").first()
    hero_forgot_password = HeroSlide.objects.filter(is_active=True, page="forgot_password").first()
    hero_otp_verify = HeroSlide.objects.filter(is_active=True, page="otp_verify").first()

    cart_count = 0
    try:
        if request.user.is_authenticated:
            cart = request.user.cart_set.first()
            if cart:
                cart_count = sum(item.quantity for item in cart.items.all())
        elif request.session.session_key:
            from apps.cart.models import Cart
            cart = Cart.objects.filter(session_key=request.session.session_key).first()
            if cart:
                cart_count = sum(item.quantity for item in cart.items.all())
    except Exception:
        pass

    return {
        "SITE_NAME": "SekhmetKarnark",
        "SITE_TAGLINE": "Sagesse Ancienne, Science Moderne",
        "SITE_TAGLINE_EN": "Ancient Wisdom, Modern Science",
        "DEBUG": settings.DEBUG,
        "CACHE_TTL": settings.CACHE_TTL,
        "hero_slides": hero_slides,
        "hero_login": hero_login,
        "hero_register": hero_register,
        "hero_forgot_password": hero_forgot_password,
        "hero_otp_verify": hero_otp_verify,
        "cart_item_count": cart_count,
    }
