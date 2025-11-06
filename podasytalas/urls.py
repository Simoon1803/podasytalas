from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, FileResponse
from django.contrib.sitemaps.views import sitemap
import os
from .sitemaps import StaticViewSitemap  # Importa tu clase del archivo sitemaps.py

# ------------------------------------------------------------
# Registrar sitemaps
# ------------------------------------------------------------
sitemaps = {
    "static": StaticViewSitemap,
}
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow:",
        "Sitemap: https://podasytalasias.cl/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

urlpatterns = [
    # ✅ Sitemap real de Django
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),

    # ✅ robots.txt
    path("robots.txt", robots_txt, name="robots"),

    # ✅ Manifest.json
    path(
        "manifest.json",
        lambda request: FileResponse(
            open(os.path.join(settings.BASE_DIR, "podasytalas", "templates", "manifest.json"), "rb"),
            content_type="application/json"
        ),
        name="manifest"
    ),

    # ✅ Admin original (acceso oculto)
    path("hidden-admin/", admin.site.urls),

    # 🌍 Sitio web público
    path("", include("web.urls")),

    # 📊 Dashboard personalizado
    path("dashboard/", include("dashboard.urls")),

    # 🔄 Redirección /admin → Dashboard
    path("admin/", RedirectView.as_view(pattern_name="dashboard:home", permanent=False)),

    # 🔐 Login personalizado
    path(
        "admin/login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True,
        ),
        name="login"
    ),

    # 🔒 Logout
    path(
        "admin/logout/",
        auth_views.LogoutView.as_view(next_page="/admin/login/"),
        name="logout"
    ),

    # 🔑 Recuperar contraseña
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            html_email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url="/reset_password_sent/"
        ),
        name="password_reset"
    ),

    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
]

# ------------------------------------------------------------
# Archivos multimedia (solo en modo DEBUG)
# ------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
