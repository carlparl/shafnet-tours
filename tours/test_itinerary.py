from django.test import TestCase
from django.urls import reverse

from .models import Itinerary, Tour


class ItineraryDisplayTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tour = Tour.objects.create(
            title="Western Uganda Journey",
            description="A sample itinerary-enabled tour.",
            duration_days=3,
            location="Western Uganda",
            target_audience="international",
        )
        Itinerary.objects.create(
            tour=cls.tour,
            day=1,
            title="Arrival and welcome",
            description="Meet the guide and begin the journey.",
            meals="Lunch and dinner",
            accommodation="Example Safari Lodge",
        )

    def test_itinerary_details_appear_on_tour_page(self):
        response = self.client.get(
            reverse("tour_detail", args=[self.tour.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Arrival and welcome")
        self.assertContains(response, "Lunch and dinner")
        self.assertContains(response, "Example Safari Lodge")