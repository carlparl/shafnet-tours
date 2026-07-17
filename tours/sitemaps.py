from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Tour


class StaticViewSitemap(Sitemap):
    pages = (
        ("home", "weekly", 1.0),
        ("domestic_tours", "weekly", 0.9),
        ("safaris", "weekly", 0.9),
        ("about", "monthly", 0.6),
        ("gallery", "weekly", 0.7),
        ("contact", "monthly", 0.6),
        ("booking_policy", "yearly", 0.4),
        ("terms_and_conditions", "yearly", 0.3),
        ("privacy_policy", "yearly", 0.3),
    )

    def items(self):
        return self.pages

    def location(self, item):
        return reverse(item[0])

    def changefreq(self, item):
        return item[1]

    def priority(self, item):
        return item[2]


class TourSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Tour.objects.all()
