from datetime import timedelta

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Booking, Tour


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    BOOKING_NOTIFICATION_EMAIL="bookings@example.com",
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": (
                "django.contrib.staticfiles.storage.StaticFilesStorage"
            ),
        },
    },
)
class PublicSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.domestic_tour = Tour.objects.create(
            title="Lake Mburo Weekend",
            description="A relaxed local escape with wildlife and landscapes.",
            price=450,
            duration_days=3,
            location="Lake Mburo",
            target_audience="domestic",
            region="western",
            is_featured=True,
        )
        cls.safari_tour = Tour.objects.create(
            title="Western Uganda Safari",
            description="A considered safari through western Uganda.",
            price=1800,
            duration_days=7,
            location="Western Uganda",
            target_audience="international",
            region="western",
            is_featured=True,
        )

    def test_public_pages_render(self):
        urls = [
            reverse("home"),
            reverse("domestic_tours"),
            reverse("safaris"),
            reverse("tour_detail", args=[self.safari_tour.slug]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Shafnet Tours")

        detail_response = self.client.get(
            reverse("tour_detail", args=[self.safari_tour.slug])
        )
        self.assertContains(detail_response, "google.com/maps")
        self.assertContains(detail_response, 'rel="canonical"')

    def test_booking_creates_record_sends_emails_and_confirms(self):
        response = self.client.post(
            reverse("tour_detail", args=[self.safari_tour.slug]),
            {
                "full_name": "Amina Traveller",
                "email": "amina@example.com",
                "phone": "+256700000000",
                "number_of_people": 2,
                "preferred_date": (
                    timezone.localdate() + timedelta(days=30)
                ),
                "message": "Please share the available options.",
                "accept_policies": "yes",
            },
        )

        self.assertRedirects(response, reverse("booking_confirmation"))
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 2)

        confirmation = self.client.get(reverse("booking_confirmation"))
        self.assertEqual(confirmation.status_code, 200)
        self.assertContains(confirmation, "Amina Traveller")

    def test_booking_rejects_past_date(self):
        response = self.client.post(
            reverse("tour_detail", args=[self.safari_tour.slug]),
            {
                "full_name": "Amina Traveller",
                "email": "amina@example.com",
                "phone": "+256700000000",
                "number_of_people": 2,
                "preferred_date": (
                    timezone.localdate() - timedelta(days=1)
                ),
                "message": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Please choose today or a future travel date.",
        )
        self.assertEqual(Booking.objects.count(), 0)

    def test_sitemap_and_robots_are_available(self):
        sitemap_response = self.client.get("/sitemap.xml")
        self.assertEqual(sitemap_response.status_code, 200)
        self.assertContains(
            sitemap_response,
            self.safari_tour.get_absolute_url(),
        )

        robots_response = self.client.get(reverse("robots_txt"))
        self.assertEqual(robots_response.status_code, 200)
        self.assertContains(robots_response, "Sitemap:")
        self.assertContains(robots_response, "/sitemap.xml")