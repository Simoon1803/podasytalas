import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from django import template

# ------------------------------------------------------------
# 📁 Directorios base
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent  # carpeta donde está manage.py

# ------------------------------------------------------------
# 🔐 Carga de variables de entorno (.env y .env.production)
# ------------------------------------------------------------
ENV_PATH = PROJECT_ROOT / ".env.production"
LOCAL_ENV_PATH = PROJECT_ROOT / ".env"

# Cargar primero el .env local (si existe)
if LOCAL_ENV_PATH.exists():
    load_dotenv(dotenv_path=LOCAL_ENV_PATH, override=False)

# Cargar luego el .env.production (si existe)
if ENV_PATH.exists():
    print(f">>> Cargando variables desde: {ENV_PATH}")
    load_dotenv(dotenv_path=ENV_PATH, override=True)
else:
    print("⚠️  Archivo .env.production no encontrado")

# ------------------------------------------------------------
# 🔐 Seguridad
# ------------------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise Exception("❌ La variable DJANGO_SECRET_KEY no está definida o está vacía.")

DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"

ALLOWED_HOSTS = ["podasytalasias.cl", "www.podasytalasias.cl", "127.0.0.1", "localhost"]

CSRF_TRUSTED_ORIGINS = [
    "https://podasytalasias.cl",
    "https://www.podasytalasias.cl",
    "http://127.0.0.1:8000"
]

# ------------------------------------------------------------
# 📦 Aplicaciones instaladas
# ------------------------------------------------------------
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

    # Apps locales
    "web",
    "dashboard",

    # Librerías externas
    "sweetify",
    "widget_tweaks",
]

SITE_ID = 1

# ------------------------------------------------------------
# ⚙️ Middleware
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# 🔗 Configuración base del proyecto
# ------------------------------------------------------------
ROOT_URLCONF = "podasytalas.urls"
WSGI_APPLICATION = "podasytalas.wsgi.application"

# ------------------------------------------------------------
# 🧱 Templates
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# 🗄️ Base de datos
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# 🗂️ Archivos estáticos y media
# ------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "podasytalas" / "static",
    BASE_DIR / "dashboard" / "static",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------------------------------
# ✉️ Configuración de correo
# ------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = f"Podas y Talas Isaías <{EMAIL_HOST_USER}>"

# ------------------------------------------------------------
# 🔐 Autenticación y login
# ------------------------------------------------------------
LOGIN_REDIRECT_URL = "/dashboard/"
LOGIN_URL = "/admin/login/"
LOGOUT_REDIRECT_URL = "/admin/login/"

# ------------------------------------------------------------
# ⚙️ Configuración adicional
# ------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SWEETIFY_SWEETALERT_LIBRARY = "sweetalert2"

# ------------------------------------------------------------
# 🧩 Filtro personalizado (add_class)
# ------------------------------------------------------------
register = template.Library()

@register.filter(name="add_class")
def add_class(field, css):
    return field.as_widget(attrs={"class": css})
