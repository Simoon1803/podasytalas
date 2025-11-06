import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from django import template


BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent  # carpeta donde está manage.py

# Cargar variables: primero .env (PC), luego .env.production (servidor) SOBREESCRIBIENDO
load_dotenv(PROJECT_ROOT / ".env", override=False)
load_dotenv(PROJECT_ROOT / ".env.production", override=True)

# ---- Seguridad ----
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"

# Hosts desde env (coma-separado)
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost"
).split(",")

# CSRF para tus dominios + dev
CSRF_TRUSTED_ORIGINS = [
    f"https://{h.strip()}" for h in ALLOWED_HOSTS if h.strip() not in ("127.0.0.1", "localhost")
] + ["http://127.0.0.1:8000"]


# ---------------------------- 📦 Apps ----------------------------
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "web",
    "dashboard",

    "sweetify",
    "widget_tweaks",
]

SITE_ID = 1

# ---------------------------- ⚙️ Middleware ----------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "podasytalas.urls"
WSGI_APPLICATION = "podasytalas.wsgi.application"

# ---------------------------- 🧱 Templates ----------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "dashboard" / "templates",
            BASE_DIR / "web" / "templates",
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---- Base de datos ----
db_url = os.getenv("DATABASE_URL")
if db_url:
    DATABASES = {"default": dj_database_url.parse(db_url, conn_max_age=600)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }

# ---------------------------- 📁 Archivos estáticos ----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "podasytalas" / "static",
    BASE_DIR / "dashboard" / "static",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------- ✉️ Email ----------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = f"Podas y Talas Isaías <{EMAIL_HOST_USER}>"

# ---------------------------- 🔐 Login ----------------------------
LOGIN_REDIRECT_URL = "/dashboard/"
LOGIN_URL = "/admin/login/"
LOGOUT_REDIRECT_URL = "/admin/login/"

# ---------------------------- ✅ Otros ----------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SWEETIFY_SWEETALERT_LIBRARY = "sweetalert2"

register = template.Library()
@register.filter(name="add_class")
def add_class(field, css):
    return field.as_widget(attrs={"class": css})
