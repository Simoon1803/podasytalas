from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return [
            'web:home',
            'web:servicios',
            'web:quienes_somos',
            'web:galeria',
            'web:contacto',
        ]

    def location(self, item):
        return reverse(item)
