from django.urls import path
from . import views

app_name = "web"

urlpatterns = [
    path("", views.home, name="home"),  # 👈 Página principal
    path('contacto/', views.contacto, name='contacto'),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('galeria/', views.galeria, name='galeria'),
    path('servicios/', views.servicios, name='servicios'),
]
