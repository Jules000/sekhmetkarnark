import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-me-in-production")
DEBUG = os.getenv("DEBUG", "False") == "True"
_allowed = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = _allowed.replace(" ", ",").split(",")

DJANGO_ENV = os.getenv("DJANGO_ENV", "local")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # Third-party
    "jazzmin",
    "django_redis",
    "imagekit",
    "modeltranslation",
    "storages",
    "django_ckeditor_5",
    "django_filters",
    "django_ratelimit",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",
    "csp",
    # Local apps
    "apps.core",
    "apps.accounts",
    "apps.blog",
    "apps.shop",
    "apps.cart",
    "apps.orders",
    "apps.payments",
    "apps.newsletter",
    "apps.contact",
    "apps.seo",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

if os.getenv("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.parse(
            os.getenv("DATABASE_URL"),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
            "NAME": os.getenv("DB_NAME", "sekhmetkarnak"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
            "CONN_MAX_AGE": 60,
            "OPTIONS": {"connect_timeout": 10},
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fr"
LANGUAGES = [
    ("fr", "Français"),
    ("en", "English"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_MAX_AGE = 31536000
WHITENOISE_AUTOREFRESH = False

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

AUTH_USER_MODEL = "accounts.User"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TRANZAK_MODE = os.getenv("TRANZAK_MODE", "sandbox")

TRANZAK_SANDBOX_APP_ID = os.getenv("TRANZAK_SANDBOX_APP_ID", "")
TRANZAK_SANDBOX_APP_KEY = os.getenv("TRANZAK_SANDBOX_APP_KEY", "")
TRANZAK_SANDBOX_WEBHOOK_SECRET = os.getenv("TRANZAK_SANDBOX_WEBHOOK_SECRET", "")

TRANZAK_LIVE_APP_ID = os.getenv("TRANZAK_LIVE_APP_ID", "")
TRANZAK_LIVE_APP_KEY = os.getenv("TRANZAK_LIVE_APP_KEY", "")
TRANZAK_LIVE_WEBHOOK_SECRET = os.getenv("TRANZAK_LIVE_WEBHOOK_SECRET", "")

if TRANZAK_MODE == "live":
    TRANZAK_APP_ID = TRANZAK_LIVE_APP_ID
    TRANZAK_APP_KEY = TRANZAK_LIVE_APP_KEY
    TRANZAK_WEBHOOK_SECRET = TRANZAK_LIVE_WEBHOOK_SECRET
    TRANZAK_API_BASE_URL = "https://api.tranzak.me/v1"
else:
    TRANZAK_APP_ID = TRANZAK_SANDBOX_APP_ID
    TRANZAK_APP_KEY = TRANZAK_SANDBOX_APP_KEY
    TRANZAK_WEBHOOK_SECRET = TRANZAK_SANDBOX_WEBHOOK_SECRET
    TRANZAK_API_BASE_URL = "https://sandbox.api.tranzak.me/v1"

TRANZAK_FRONTEND_SDK_URL = "https://cdn.tranzak.me/sdk.js"

BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "contact@sekhmetkarnak.com")
CONTACT_EMAIL_ADMIN = os.getenv("CONTACT_EMAIL_ADMIN", "admin@sekhmetkarnak.com")

_redis_url = os.getenv("REDIS_URL", "")

if _redis_url:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": _redis_url,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
                "IGNORE_EXCEPTIONS": True,
                "CONNECTION_POOL_KWARGS": {"max_connections": 50},
                "SOCKET_CONNECT_TIMEOUT": 5,
                "SOCKET_TIMEOUT": 5,
            },
            "KEY_PREFIX": "sk",
            "TIMEOUT": 300,
        },
        "sessions": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": _redis_url + "/1",
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
            "TIMEOUT": 86400,
        },
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "sessions"
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "sk-default",
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.db"

CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = "sk"

JAZZMIN_SETTINGS = {
    "site_title": "SekhmetKarnark Admin",
    "site_header": "SekhmetKarnark",
    "site_brand": "SekhmetKarnark",
    "site_logo": "icons/sekhmetkarnark-logo.svg",
    "site_logo_classes": "img-circle",
    "site_icon": "icons/sekhmetkarnark-logo.svg",
    "welcome_sign": "Bienvenue dans l'administration SekhmetKarnark",
    "copyright": "SekhmetKarnark ©",
    "search_model": ["accounts.User", "shop.Product", "blog.Article"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Accueil", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Voir le site", "url": "/", "new_window": True},
    ],
    "usermenu_links": [
        {"name": "Voir le site", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "core",
        "shop",
        "blog",
        "orders",
        "payments",
        "accounts",
        "contact",
        "newsletter",
        "cart",
        "seo",
        "auth",
    ],
    "custom_links": {},
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "accounts.User": "fas fa-user-circle",
        "core.HeroSlide": "fas fa-images",
        "shop.Product": "fas fa-cube",
        "shop.Category": "fas fa-tags",
        "blog.Article": "fas fa-newspaper",
        "blog.Category": "fas fa-tag",
        "blog.Tag": "fas fa-hashtag",
        "orders.Order": "fas fa-shopping-cart",
        "orders.OrderItem": "fas fa-box",
        "payments.TranzakTransaction": "fas fa-credit-card",
        "contact.ContactMessage": "fas fa-envelope",
        "newsletter.Subscriber": "fas fa-bell",
        "cart.Cart": "fas fa-shopping-bag",
        "cart.CartItem": "fas fa-box-open",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": "css/admin.css",
    "custom_js": None,
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.User": "collapsible",
        "accounts.User": "collapsible",
    },
    "language_chooser": True,
}

CKEDITOR_5_CONFIGS = {
    "default": {
        "language": {"ui": "fr", "content": "fr"},
        "toolbar": [
            "heading", "|",
            "bold", "italic", "underline", "strikethrough", "subscript", "superscript", "|",
            "fontColor", "fontBackgroundColor", "fontSize", "fontFamily", "|",
            "alignment", "|",
            "bulletedList", "numberedList", "|",
            "outdent", "indent", "|",
            "blockQuote", "link", "imageUpload", "mediaEmbed", "insertTable", "|",
            "undo", "redo", "|",
            "sourceEditing", "removeFormat", "|",
            "specialCharacters", "horizontalLine", "pageBreak",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative", "imageStyle:inline",
                "imageStyle:block", "imageStyle:side",
                "linkImage",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn", "tableRow", "mergeTableCells",
                "tableCellProperties", "tableProperties",
            ],
        },
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph", "class": "ck-heading_paragraph"},
                {"model": "heading1", "view": "h1", "title": "Heading 1", "class": "ck-heading_heading1"},
                {"model": "heading2", "view": "h2", "title": "Heading 2", "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Heading 3", "class": "ck-heading_heading3"},
                {"model": "heading4", "view": "h4", "title": "Heading 4", "class": "ck-heading_heading4"},
            ],
        },
        "list": {
            "properties": {"styles": True, "startIndex": True, "reversed": True},
        },
    },
    "minimal": {
        "language": {"ui": "fr", "content": "fr"},
        "toolbar": [
            "bold", "italic", "link", "bulletedList", "numberedList", "undo", "redo",
        ],
    },
}

CKEDITOR_5_FILE_STORAGE = "django_ckeditor_5.storage.CKEditor5Storage"
CKEDITOR_5_CUSTOM_CSS = "css/admin.css"

CACHE_TTL = {
    "homepage": 60 * 15,
    "article_list": 60 * 10,
    "article_detail": 60 * 30,
    "product_list": 60 * 10,
    "product_detail": 60 * 20,
    "category_list": 60 * 60,
    "static_pages": 60 * 60 * 24,
    "disease_list": 60 * 60 * 2,
    "navbar": 60 * 60 * 6,
    "footer": 60 * 60 * 12,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
