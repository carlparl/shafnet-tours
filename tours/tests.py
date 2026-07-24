from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace

from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import (
    Booking,
    CompanyCredential,
    ContactMessage,
    GalleryImage,
    TeamMember,
    Testimonial,
    Tour,
)
from .templatetags.image_urls import optimized_image_url


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
        self.assertContains(
            response,
            'images/page-heroes/safari-hero.jpg',
        )
        self.assertContains(response, 'property="og:image"')
        self.assertContains(
            response,
            'name="twitter:card" content="summary_large_image"',
        )
        self.assertContains(response, 'css/site-motion.css')
        self.assertContains(response, 'js/site-motion.js')
        self.assertContains(response, 'class="scroll-progress"')
        self.assertContains(response, 'data-back-to-top')
        self.assertNotContains(response, "images.unsplash.com")
        self.assertContains(response, 'class="is-active" aria-current="page"')

    def test_page_heroes_use_local_uganda_images(self):
        stylesheet_path = finders.find("css/site.css")

        self.assertIsNotNone(stylesheet_path)
        stylesheet = Path(stylesheet_path).read_text(encoding="utf-8")
        expected_images = [
            "../images/uganda-lake-landscape-hero-hd.jpg",
            "../images/page-heroes/about-hero.jpg",
            "../images/page-heroes/gallery-hero.jpg",
            "../images/page-heroes/safari-hero.jpg",
        ]

        for image_path in expected_images:
            with self.subTest(image_path=image_path):
                self.assertIn(image_path, stylesheet)

        self.assertNotIn("images.unsplash.com", stylesheet)

    def test_cloudinary_image_urls_are_optimized(self):
        image = SimpleNamespace(
            url=(
                "https://res.cloudinary.com/iuscby6h/image/upload/"
                "v1/media/tours/example"
            ),
        )

        self.assertEqual(
            optimized_image_url(image, 800),
            (
                "https://res.cloudinary.com/iuscby6h/image/upload/"
                "c_limit,w_800/f_auto/q_auto/"
                "v1/media/tours/example"
            ),
        )

    def test_non_cloudinary_image_urls_are_unchanged(self):
        image = SimpleNamespace(url="/media/tours/example.jpg")

        self.assertEqual(
            optimized_image_url(image, 800),
            "/media/tours/example.jpg",
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

    def test_verified_credibility_content_renders_from_admin_records(self):
        CompanyCredential.objects.create(
            name="Tour Operator Registration",
            issuer="Example Tourism Registry",
            identifier="REG-2026-001",
            description="Current public operator record.",
            verification_url="https://registry.example.com/shafnet",
            valid_until=timezone.localdate() + timedelta(days=365),
            is_active=True,
        )
        TeamMember.objects.create(
            name="Amina Guide",
            role="Safari planner",
            bio="Plans considered Uganda journeys for local and international guests.",
            qualifications="Certified destination specialist",
            languages="English and Luganda",
            is_active=True,
        )
        Testimonial.objects.create(
            name="Daniel Traveller",
            location="Nairobi, Kenya",
            message="The route was clear and the support was responsive.",
            rating=4,
            tour_name="Western Uganda Safari",
            travel_date=timezone.localdate(),
            source_name="Example Reviews",
            source_url="https://reviews.example.com/shafnet/daniel",
            is_verified=True,
            is_active=True,
        )

        home_response = self.client.get(reverse("home"))
        self.assertContains(home_response, "Credentials you can verify")
        self.assertContains(home_response, "REG-2026-001")
        self.assertContains(home_response, "Valid until")
        self.assertContains(home_response, "Source checked")
        self.assertContains(home_response, "View on Example Reviews")
        self.assertContains(home_response, "★★★★☆")

        about_response = self.client.get(reverse("about"))
        self.assertContains(about_response, "The people behind your journey")
        self.assertContains(about_response, "Amina Guide")
        self.assertContains(about_response, "Certified destination specialist")
        self.assertContains(about_response, "Check our credentials directly")

    def test_unverified_or_inactive_credibility_content_stays_hidden(self):
        CompanyCredential.objects.create(
            name="Inactive credential",
            verification_url="https://registry.example.com/inactive",
            is_active=False,
        )
        CompanyCredential.objects.create(
            name="Expired credential",
            verification_url="https://registry.example.com/expired",
            valid_until=timezone.localdate() - timedelta(days=1),
            is_active=True,
        )
        TeamMember.objects.create(
            name="Inactive profile",
            role="Planner",
            bio="This profile is not approved for publication.",
            is_active=False,
        )
        Testimonial.objects.create(
            name="Unverified reviewer",
            message="This review has not been source checked.",
            rating=5,
            source_name="Example Reviews",
            source_url="https://reviews.example.com/unverified",
            is_verified=False,
            is_active=True,
        )
        Testimonial.objects.create(
            name="Missing source reviewer",
            message="This verified flag lacks a public source.",
            rating=5,
            is_verified=True,
            is_active=True,
        )

        home_response = self.client.get(reverse("home"))
        self.assertNotContains(home_response, "Inactive credential")
        self.assertNotContains(home_response, "Expired credential")
        self.assertNotContains(home_response, "Unverified reviewer")
        self.assertNotContains(home_response, "Missing source reviewer")
        self.assertNotContains(home_response, "Credentials you can verify")

        about_response = self.client.get(reverse("about"))
        self.assertNotContains(about_response, "Inactive profile")
        self.assertNotContains(about_response, "Check our credentials directly")

    def test_testimonial_rating_must_be_between_one_and_five(self):
        testimonial = Testimonial(
            name="Invalid rating",
            message="A rating outside the public scale should be rejected.",
            rating=6,
        )

        with self.assertRaises(ValidationError):
            testimonial.full_clean()

    def test_expanded_safari_catalogue_has_complete_itineraries(self):
        expected_days = {
            "3-day-bwindi-gorilla-trekking": 3,
            "3-day-kibale-chimpanzee-experience": 3,
            "5-day-kidepo-valley-wilderness-safari": 5,
            "5-day-gorilla-and-queen-elizabeth-safari": 5,
            "7-day-western-uganda-wildlife-and-primates": 7,
            "10-day-uganda-grand-safari": 10,
        }

        for slug, day_count in expected_days.items():
            with self.subTest(slug=slug):
                tour = Tour.objects.get(slug=slug)
                self.assertTrue(tour.is_active)
                self.assertEqual(tour.target_audience, "international")
                self.assertEqual(tour.itineraries.count(), day_count)
                self.assertTrue(tour.inclusions)
                self.assertTrue(tour.exclusions)

    def test_catalogue_filters_and_sorting(self):
        response = self.client.get(
            reverse("safaris"),
            {
                "region": "northern",
                "duration": "4-6",
                "style": "focused",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "5-Day Kidepo Valley Wilderness Safari")
        self.assertNotContains(response, self.safari_tour.title)
        self.assertTrue(response.context["filters_applied"])
        self.assertEqual(
            tuple(response.context["style_choices"]),
            (
                ("focused", "Focused safari"),
                ("combo", "Two-park combination"),
                ("circuit", "Multi-park circuit"),
            ),
        )

        longest_response = self.client.get(
            reverse("safaris"),
            {"sort": "longest"},
        )
        longest_tours = list(longest_response.context["tours"])
        self.assertEqual(longest_tours[0].slug, "10-day-uganda-grand-safari")

        domestic_response = self.client.get(
            reverse("domestic_tours"),
            {"style": "focused"},
        )
        self.assertEqual(
            tuple(domestic_response.context["style_choices"]),
            (
                ("transfer", "Transfer service"),
                ("day_trip", "Day experience"),
                ("short_escape", "Short escape"),
            ),
        )
        self.assertEqual(domestic_response.context["selected_style"], "")

    def test_safari_packages_have_distinct_public_positioning(self):
        expected_styles = {
            "3-day-queen-elizabeth-safari": "focused",
            "4-day-murchison-falls-adventure": "focused",
            "3-day-bwindi-gorilla-trekking": "focused",
            "3-day-kibale-chimpanzee-experience": "focused",
            "5-day-gorilla-and-queen-elizabeth-safari": "combo",
            "5-day-kidepo-valley-wilderness-safari": "focused",
            "7-day-western-uganda-wildlife-and-primates": "circuit",
            "10-day-uganda-grand-safari": "circuit",
        }

        for slug, journey_style in expected_styles.items():
            with self.subTest(slug=slug):
                tour = Tour.objects.get(slug=slug)
                self.assertEqual(tour.journey_style, journey_style)
                self.assertTrue(tour.best_for)

        response = self.client.get(reverse("safaris"))
        self.assertContains(response, "Focused safari")
        self.assertContains(response, "Two-park combination")
        self.assertContains(response, "Multi-park circuit")
        self.assertContains(response, "Best for:")

    def test_old_bwindi_url_redirects_to_realistic_three_day_package(self):
        response = self.client.get(
            reverse(
                "tour_detail",
                kwargs={"slug": "2-day-bwindi-gorilla-trekking"},
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "tour_detail",
                kwargs={"slug": "3-day-bwindi-gorilla-trekking"},
            ),
            status_code=301,
            fetch_redirect_response=False,
        )

        new_response = self.client.get(
            reverse(
                "tour_detail",
                kwargs={"slug": "3-day-bwindi-gorilla-trekking"},
            )
        )
        self.assertEqual(new_response.status_code, 200)
        self.assertContains(new_response, "3-Day Bwindi Gorilla Trekking")
        self.assertContains(new_response, "3 days")

    def test_inactive_tour_is_hidden_from_public_pages_and_sitemap(self):
        inactive_tour = Tour.objects.create(
            title="Unpublished Safari Draft",
            description="This draft must remain private.",
            duration_days=4,
            location="Uganda",
            target_audience="international",
            is_active=False,
        )

        listing_response = self.client.get(reverse("safaris"))
        self.assertNotContains(listing_response, inactive_tour.title)

        detail_response = self.client.get(inactive_tour.get_absolute_url())
        self.assertEqual(detail_response.status_code, 404)

        sitemap_response = self.client.get("/sitemap.xml")
        self.assertNotContains(
            sitemap_response,
            inactive_tour.get_absolute_url(),
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
