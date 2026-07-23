from datetime import timedelta
from pathlib import Path

from django.contrib.staticfiles import finders
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Booking, ContactMessage, GalleryImage, Tour


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
            price=450000,
            currency="UGX",
            price_basis="per_group",
            price_is_from=False,
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
            currency="USD",
            price_basis="per_person",
            price_is_from=True,
            duration_days=7,
            location="Western Uganda",
            target_audience="international",
            region="western",
            is_featured=True,
        )
        cls.gallery_image = GalleryImage.objects.create(
            title="Kazinga Channel",
            caption="A quiet afternoon on the water.",
            image="gallery/kazinga-channel.jpg",
        )

    def test_public_pages_render(self):
        urls = [
            reverse("home"),
            reverse("domestic_tours"),
            reverse("safaris"),
            reverse("about"),
            reverse("gallery"),
            reverse("contact"),
            reverse("privacy_policy"),
            reverse("terms_and_conditions"),
            reverse("booking_policy"),
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

        home_response = self.client.get(reverse("home"))
        self.assertContains(home_response, "How we plan your journey")
        self.assertContains(home_response, "UGX 450,000 per group")
        self.assertContains(home_response, "From USD 1,800 per person")

        about_response = self.client.get(reverse("about"))
        self.assertContains(
            about_response,
            "Your journey starts with being heard.",
        )

        domestic_response = self.client.get(reverse("domestic_tours"))
        self.assertContains(domestic_response, "UGX 450,000 per group")

        self.assertContains(detail_response, "USD 1,800")
        self.assertContains(detail_response, "per person")

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
        for email in mail.outbox:
            self.assertIn("From USD 1,800 per person", email.body)

        confirmation = self.client.get(reverse("booking_confirmation"))
        self.assertEqual(confirmation.status_code, 200)
        self.assertContains(confirmation, "Amina Traveller")
        self.assertContains(confirmation, "From USD 1,800 per person")

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

    def test_contact_creates_record_sends_emails_and_redirects(self):
        response = self.client.post(
            reverse("contact"),
            {
                "full_name": "Amina Traveller",
                "email": "amina@example.com",
                "subject": "Custom Uganda journey",
                "message": "Please help me plan a seven-day trip.",
            },
        )

        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 2)

    def test_contact_rejects_incomplete_submission(self):
        response = self.client.post(
            reverse("contact"),
            {
                "full_name": "Amina Traveller",
                "email": "not-an-email",
                "message": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)


    def test_homepage_title_and_motion_markup_are_valid(self):
        response = self.client.get(reverse("home"))

        self.assertContains(
            response,
            "<title>Shafnet Tours | Uganda Tours &amp; Safaris</title>",
            html=True,
        )
        self.assertNotContains(response, "<title><script")
        self.assertContains(response, 'class="hero-slides"')
        self.assertEqual(
            response.content.decode().count("hero-slide hero-slide-"),
            3,
        )
        self.assertEqual(
            response.content.decode().count("data-hero-slide"),
            4,
        )
        self.assertContains(response, 'data-hero-toggle')
        self.assertContains(response, 'class="hero-scroll-cue"')
        self.assertContains(
            response,
            'images/uganda-lake-landscape-hero-hd.jpg',
        )
        self.assertContains(response, 'css/site-motion.css')
        self.assertContains(response, 'js/site-motion.js')
        self.assertContains(response, 'class="scroll-progress"')
        self.assertContains(response, 'data-back-to-top')
        self.assertNotContains(response, "images.unsplash.com")
        self.assertContains(response, 'class="is-active" aria-current="page"')

    def test_domestic_listing_hero_uses_local_uganda_image(self):
        stylesheet_path = finders.find("css/site.css")

        self.assertIsNotNone(stylesheet_path)
        stylesheet = Path(stylesheet_path).read_text(encoding="utf-8")
        self.assertIn(
            '../images/uganda-lake-landscape-hero-hd.jpg',
            stylesheet,
        )
        self.assertNotIn(
            "images.unsplash.com/photo-1501854140801-50d01698950b",
            stylesheet,
        )

    def test_site_wide_motion_controls_render_on_public_pages(self):
        urls = [
            reverse("home"),
            reverse("domestic_tours"),
            reverse("safaris"),
            reverse("about"),
            reverse("gallery"),
            reverse("contact"),
            reverse("privacy_policy"),
            reverse("terms_and_conditions"),
            reverse("booking_policy"),
            reverse("tour_detail", args=[self.safari_tour.slug]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, 'css/site-motion.css')
                self.assertContains(response, 'js/site-motion.js')
                self.assertContains(response, 'class="scroll-progress"')
                self.assertContains(response, 'data-back-to-top')

        policy_response = self.client.get(reverse("privacy_policy"))
        self.assertContains(policy_response, 'class="policy-nav"')
        self.assertContains(policy_response, 'href="#information-we-collect"')

        gallery_response = self.client.get(reverse("gallery"))
        self.assertContains(gallery_response, 'data-gallery-item')
        self.assertContains(gallery_response, 'data-gallery-open')

    def test_booking_requires_policy_consent(self):
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
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Please accept the Terms, Booking Policy and Privacy Policy.",
        )
        self.assertEqual(Booking.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_booking_honeypot_rejects_bot_submission(self):
        response = self.client.post(
            reverse("tour_detail", args=[self.safari_tour.slug]),
            {
                "full_name": "Automated Submission",
                "email": "bot@example.com",
                "phone": "+256700000000",
                "number_of_people": 2,
                "preferred_date": (
                    timezone.localdate() + timedelta(days=30)
                ),
                "message": "Automated message.",
                "website": "https://spam.invalid",
                "accept_policies": "yes",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_contact_honeypot_rejects_bot_submission(self):
        response = self.client.post(
            reverse("contact"),
            {
                "full_name": "Automated Submission",
                "email": "bot@example.com",
                "subject": "Spam",
                "message": "Automated message.",
                "website": "https://spam.invalid",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_duplicate_tour_titles_receive_unique_slugs(self):
        first = Tour.objects.create(
            title="Murchison Falls Safari",
            description="First itinerary.",
            duration_days=3,
            location="Murchison Falls",
        )
        second = Tour.objects.create(
            title="Murchison Falls Safari",
            description="Second itinerary.",
            duration_days=4,
            location="Murchison Falls",
        )

        self.assertEqual(first.slug, "murchison-falls-safari")
        self.assertEqual(second.slug, "murchison-falls-safari-2")

    def test_empty_homepage_catalogue_states_render(self):
        Tour.objects.all().delete()

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Domestic experiences are being prepared",
        )
        self.assertContains(
            response,
            "Your ideal safari can start here",
        )

    def test_sitemap_and_robots_are_available(self):
        sitemap_response = self.client.get("/sitemap.xml")
        self.assertEqual(sitemap_response.status_code, 200)
        self.assertContains(
            sitemap_response,
            self.safari_tour.get_absolute_url(),
        )
        self.assertContains(sitemap_response, reverse("about"))
        self.assertContains(sitemap_response, reverse("gallery"))
        self.assertContains(sitemap_response, reverse("contact"))

        robots_response = self.client.get(reverse("robots_txt"))
        self.assertEqual(robots_response.status_code, 200)
        self.assertContains(robots_response, "Sitemap:")
        self.assertContains(robots_response, "/sitemap.xml")
