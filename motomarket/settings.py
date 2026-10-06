import os
from pathlib import Path

import dj_database_url
from django.templatetags.static import static
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-solo-para-desarrollo-local")
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = []
RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_HOST:
    ALLOWED_HOSTS.append(RENDER_HOST)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_HOST}")

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "core",
    "usuarios",
    "catalogo",
    "carrito",
    "pedidos",
    "pruebas",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "motomarket.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "carrito.context_processors.carrito",
                "core.context_processors.tienda",
            ],
        },
    },
]

WSGI_APPLICATION = "motomarket.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

AUTH_USER_MODEL = "usuarios.Usuario"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "usuarios:login"
LOGIN_REDIRECT_URL = "core:inicio"
LOGOUT_REDIRECT_URL = "core:inicio"

LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
LOCALE_PATHS = [BASE_DIR / "locale"]
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        if DEBUG
        else "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

AUTHENTICATION_BACKENDS = ["usuarios.backends.UsuarioOCorreoBackend"]

CORS_ALLOW_ALL_ORIGINS = True
CORS_URLS_REGEX = r"^/api/.*$"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "API de MotoMarket",
    "DESCRIPTION": (
        "API REST de la tienda MotoMarket. La consulta es pública; crear, editar y "
        "eliminar requiere un usuario administrador (botón Authorize, basicAuth)."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

UNFOLD = {
    "SITE_TITLE": "MotoMarket",
    "SITE_HEADER": "MotoMarket",
    "SITE_SUBHEADER": "Panel del concesionario",
    "SITE_URL": "/",
    "SITE_LOGO": lambda request: static("img/logo.png"),
    "SITE_ICON": lambda request: static("img/emblema.png"),
    "SITE_SYMBOL": "two_wheeler",
    "SITE_FAVICONS": [
        {"rel": "icon", "sizes": "any", "type": "image/x-icon", "href": lambda request: static("img/favicon.ico")},
    ],
    "SHOW_HISTORY": False,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "THEME": "dark",
    "DASHBOARD_CALLBACK": "core.panel.resumen",
    "STYLES": [lambda request: static("css/panel.css")],
    "COLORS": {
        "primary": {
            "50": "#ecffec",
            "100": "#d2ffd2",
            "200": "#a6ffa6",
            "300": "#6bff6b",
            "400": "#2df52d",
            "500": "#00de00",
            "600": "#00b800",
            "700": "#009100",
            "800": "#067206",
            "900": "#0a5e0a",
            "950": "#003500",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "General",
                "items": [
                    {"title": "Inicio", "icon": "dashboard", "link": reverse_lazy("admin:index")},
                    {"title": "Ver la tienda", "icon": "storefront", "link": "/", "active": False},
                    {"title": "Reporte de ventas", "icon": "monitoring", "link": reverse_lazy("core:reporte_ventas")},
                ],
            },
            {
                "title": "Tienda",
                "items": [
                    {"title": "Motos", "icon": "two_wheeler", "link": reverse_lazy("admin:catalogo_moto_changelist")},
                    {"title": "Marcas", "icon": "sell", "link": reverse_lazy("admin:catalogo_marca_changelist")},
                    {"title": "Categorías", "icon": "category", "link": reverse_lazy("admin:catalogo_categoria_changelist")},
                ],
            },
            {
                "title": "Ventas",
                "items": [
                    {
                        "title": "Pedidos",
                        "icon": "receipt_long",
                        "link": reverse_lazy("admin:pedidos_pedido_changelist"),
                        "badge": "core.panel.pedidos_por_atender",
                    },
                    {"title": "Pagos", "icon": "payments", "link": reverse_lazy("admin:pedidos_pago_changelist")},
                ],
            },
            {
                "title": "Clientes",
                "items": [
                    {
                        "title": "Pruebas de manejo",
                        "icon": "event_available",
                        "link": reverse_lazy("admin:pruebas_solicitudprueba_changelist"),
                        "badge": "core.panel.pruebas_pendientes",
                    },
                    {"title": "Usuarios", "icon": "group", "link": reverse_lazy("admin:usuarios_usuario_changelist")},
                    {"title": "Reseñas", "icon": "reviews", "link": reverse_lazy("admin:catalogo_resena_changelist")},
                ],
            },
        ],
    },
}
