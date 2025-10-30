from django.urls import path
from dashboard import views

app_name = "dashboard"

urlpatterns = [
    # ---------------------------
    # 🌿 Inicio del panel
    # ---------------------------
    path("", views.dashboard_home, name="home"),

    # ---------------------------
    # ✂️ Servicios
    # ---------------------------
    path("services/", views.service_list, name="service_list"),
    path("services/add/", views.service_add, name="service_add"),
    path("services/edit/<int:pk>/", views.service_edit, name="service_edit"),
    path("services/delete/<int:pk>/", views.service_delete, name="service_delete"),

    # ---------------------------
    # 🖼️ Galería
    # ---------------------------
    path("gallery/", views.gallery_list, name="gallery_list"),
    path("gallery/add/", views.gallery_add, name="gallery_add"),
    path("gallery/edit/<int:pk>/", views.gallery_edit, name="gallery_edit"),
    path("gallery/delete/<int:pk>/", views.gallery_delete, name="gallery_delete"),

    # ---------------------------
    # 🎬 Videos (nuevo sistema con archivos)
    # ---------------------------
    path("videos/", views.video_list, name="video_list"),
    path("videos/add/", views.video_add, name="video_add"),
    path("videos/edit/<int:pk>/", views.video_edit, name="video_edit"),
    path("videos/delete/<int:pk>/", views.video_delete, name="video_delete"),



    # ---------------------------
    # 👥 Quiénes Somos
    # ---------------------------
    path("about/", views.about_list, name="about_list"),
    path("about/add/", views.about_add, name="about_add"),
    path("about/edit/<int:pk>/", views.about_edit, name="about_edit"),
    path("about/image/add/", views.aboutimage_add, name="aboutimage_add"),
    path("about/image/delete/<int:pk>/", views.aboutimage_delete, name="aboutimage_delete"),

    # ---------------------------
    # 🧑‍🤝‍🧑 Equipo de Trabajo
    # ---------------------------
    path("team/", views.team_list, name="team_list"),
    path("team/add/", views.team_add, name="team_add"),
    path("team/edit/<int:pk>/", views.team_edit, name="team_edit"),
    path("team/delete/<int:pk>/", views.team_delete, name="team_delete"),

    # ---------------------------
    # 💼 Presupuestos
    # ---------------------------
    path("budgets/", views.budget_list, name="budget_list"),
    path("budgets/delete/<int:pk>/", views.budget_delete, name="budget_delete"),

    # ---------------------------
    # 🚪 Cerrar sesión
    # ---------------------------
    path("logout/", views.logout_view, name="logout_view"),
]
