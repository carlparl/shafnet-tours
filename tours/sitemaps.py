from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Tour


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ["home", "domestic_tours", "safaris"]

    def location(self, item):
        return reverse(item)


class TourSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Tour.objects.all()

    def lastmod(self, tour):
        return tour.created_at
