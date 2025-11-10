from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            'web:home',
            'web:contacto',
            'web:quienes_somos',
            'web:galeria',
            'web:servicios',
            # Agrega favicon
            'web:favicon',
        ]

    def location(self, item):
        if item == 'web:favicon':
            return '/favicon.ico'
        return reverse(item)
