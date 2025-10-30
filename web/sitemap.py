from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ["web:home", "web:servicios", "web:galeria", "web:quienes_somos", "web:contacto"]

    def location(self, item):
        return reverse(item)
