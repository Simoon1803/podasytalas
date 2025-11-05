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
        ]

    def location(self, item):
        return reverse(item)
