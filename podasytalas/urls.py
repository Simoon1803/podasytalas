from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView,  TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse
import os

from podasytalas.settings import BASE_DIR

urlpatterns = [

   

    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain"
    )),

    path("sitemap.xml", TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
     
     path("manifest.json", lambda request: FileResponse(
        open(os.path.join(BASE_DIR, "podasytalas", "templates", "manifest.json"), "rb"),
        content_type="application/json"
    )),
    # ----------------------------
    # 🔒 Admin original de Django (oculto)
    # ----------------------------
    path('hidden-admin/', admin.site.urls),

    # ----------------------------
    # 🌍 Sitio web público (home principal del cliente)
    # ----------------------------
    path('', include('web.urls')),

    # ----------------------------
    # 📊 Panel personalizado (administrador)
    # ----------------------------
    path('dashboard/', include('dashboard.urls')),

    # ----------------------------
    # 🌿 Redirección del alias "admin" al dashboard
    # ----------------------------
    path('admin/', RedirectView.as_view(pattern_name='dashboard:home', permanent=False)),

    # ----------------------------
    # 🔐 Autenticación personalizada
    # ----------------------------
    path(
        'admin/login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html',
            redirect_authenticated_user=True,  # 👈 redirige al dashboard si ya está logueado
        ),
        name='login'
    ),

    # ----------------------------
    # 🚪 Cerrar sesión → redirige al login personalizado
    # ----------------------------
    path(
        'admin/logout/',
        auth_views.LogoutView.as_view(next_page='/admin/login/'),
        name='logout'
    ),

    # ----------------------------
    # 🔑 Recuperación de contraseña personalizada
    # ----------------------------
    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            html_email_template_name='registration/password_reset_email.html',  # 👈 versión HTML
            subject_template_name='registration/password_reset_subject.txt',
            success_url='/reset_password_sent/'
        ),
        name='password_reset'
    ),

    path(
        'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]

# ----------------------------
# 🖼️ Archivos multimedia (videos, imágenes, etc.)
# ----------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
