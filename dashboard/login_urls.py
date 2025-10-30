from django.urls import path
from . import auth_views_custom

urlpatterns = [
    path('', auth_views_custom.custom_login, name='login'),
]
