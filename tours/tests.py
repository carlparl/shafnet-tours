from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .forms import BookingForm
from .models import Booking, ContactMessage, Tour


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    BOOKING_NOTIFICATION_EMAIL='bookings@example.com',
    STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    },
)
class PublicSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.domestic_tour = Tour.objects.create(
            title='Lake Mburo Weekend',
            description='A relaxed local escape with wildlife and open landscapes.',
            price=450,
            duration_days=3,
            location='Lake Mburo',
            target_audience='domestic',
            region='western',
            is_featured=True,
        )
        cls.safari_tour = Tour.objects.create(
            title='Western Uganda Safari',
            description='A considered safari through western Uganda.',
            price=1800,
            duration_days=7,
            location='Western Uganda',
            target_audience='international',
            region='western',
            is_featured=True,
        )

    def test_public_pages_render(self):
        urls = [
            reverse('home'),
            reverse('tour_list'),
            reverse('gallery'),
            reverse('about'),
            reverse('contact'),
            reverse('tour_detail', args=[self.safari_tour.slug]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'css/site.css')
                self.assertContains(response, 'Shafnet Tours')

    def test_tour_filters_accept_known_values(self):
        response = self.client.get(reverse('tour_list'), {
            'audience': 'international',
            'region': 'western',
        })

        self.assertContains(response, self.safari_tour.title)
        self.assertNotContains(response, self.domestic_tour.title)
        self.assertEqual(response.context['current_region'], 'western')

    def test_tour_filters_ignore_unknown_values(self):
        response = self.client.get(reverse('tour_list'), {
            'audience': 'unknown',
            'region': 'unknown',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['current_audience'])
        self.assertIsNone(response.context['current_region'])
        self.assertEqual(response.context['tours'].count(), 2)

    def test_contact_form_saves_and_redirects(self):
        response = self.client.post(reverse('contact'), {
            'full_name': 'Amina Traveller',
            'email': 'amina@example.com',
            'subject': 'Safari enquiry',
            'message': 'I would like help planning a trip.',
        })

        self.assertRedirects(response, reverse('contact'))
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_booking_form_rejects_past_date(self):
        form = BookingForm(data={
            'full_name': 'Amina Traveller',
            'email': 'amina@example.com',
            'phone': '+256700000000',
            'number_of_people': 2,
            'preferred_date': timezone.localdate() - timedelta(days=1),
            'message': '',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('preferred_date', form.errors)

    @patch('tours.views.send_mail', side_effect=RuntimeError('mail unavailable'))
    def test_booking_is_kept_when_notification_email_fails(self, _send_mail):
        response = self.client.post(
            reverse('tour_detail', args=[self.safari_tour.slug]),
            {
                'full_name': 'Amina Traveller',
                'email': 'amina@example.com',
                'phone': '+256700000000',
                'number_of_people': 2,
                'preferred_date': timezone.localdate() + timedelta(days=30),
                'message': 'Window seat if possible.',
            },
        )

        self.assertRedirects(response, reverse('tour_detail', args=[self.safari_tour.slug]))
        self.assertEqual(Booking.objects.count(), 1)
