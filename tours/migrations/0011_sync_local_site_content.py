from django.db import migrations


TOURS = [
    {
        "slug": "3-day-queen-elizabeth-safari",
        "title": "3-Day Queen Elizabeth Safari",
        "description": (
            "Experience the landscapes and wildlife of Queen Elizabeth National Park "
            "on a three-day journey from Kampala or Entebbe. Travel through western "
            "Uganda, explore the Kasenyi plains on a guided game drive, and enjoy a "
            "boat cruise along the Kazinga Channel."
        ),
        "price": None,
        "currency": "USD",
        "price_basis": "per_person",
        "price_is_from": True,
        "duration_days": 3,
        "location": "Queen Elizabeth National Park",
        "target_audience": "international",
        "region": "western",
        "is_featured": True,
    },
    {
        "slug": "4-day-murchison-falls-adventure",
        "title": "4-Day Murchison Falls Adventure",
        "description": (
            "Discover the mighty Murchison Falls, where the Nile River forces its way "
            "through a narrow gorge. This trip includes game drives in Murchison Falls "
            "National Park, a boat safari to the base of the falls, and visits to the "
            "top of the falls. Great for nature and photography enthusiasts."
        ),
        "price": None,
        "currency": "USD",
        "price_basis": "per_person",
        "price_is_from": True,
        "duration_days": 4,
        "location": "Murchison Falls National Park",
        "target_audience": "international",
        "region": "northern",
        "is_featured": True,
    },
    {
        "slug": "2-day-bwindi-gorilla-trekking",
        "title": "2-Day Bwindi Gorilla Trekking",
        "description": (
            "An unforgettable experience tracking the endangered mountain gorillas "
            "in Bwindi Impenetrable Forest. This short but impactful trip includes a "
            "guided gorilla trek, community visit, and scenic views of the Virunga "
            "Mountains. A bucket-list adventure for many international travelers."
        ),
        "price": None,
        "currency": "USD",
        "price_basis": "per_person",
        "price_is_from": True,
        "duration_days": 2,
        "location": "Bwindi Impenetrable Forest",
        "target_audience": "international",
        "region": "western",
        "is_featured": True,
    },
    {
        "slug": "entebbe-airport-transfer",
        "title": "Entebbe Airport Transfer",
        "description": (
            "Reliable and comfortable airport pickup and drop-off service between "
            "Entebbe International Airport and Kampala or any hotel in the city. "
            "Professional drivers, clean vehicles, and 24/7 availability. Ideal for "
            "both locals and visitors."
        ),
        "price": None,
        "currency": "UGX",
        "price_basis": "per_person",
        "price_is_from": True,
        "duration_days": 1,
        "location": "Entebbe International Airport",
        "target_audience": "domestic",
        "region": None,
        "is_featured": True,
    },
    {
        "slug": "5-day-ssese-islands-beach-escape",
        "title": "5-Day Ssese Islands Beach Escape",
        "description": (
            "Relax and unwind on the beautiful Ssese Islands in Lake Victoria. Enjoy "
            "white sandy beaches, swimming, boat rides, fresh lake fish, and a peaceful "
            "island atmosphere. Perfect weekend or short holiday getaway for families "
            "and couples."
        ),
        "price": None,
        "currency": "UGX",
        "price_basis": "per_person",
        "price_is_from": True,
        "duration_days": 5,
        "location": "Ssese Islands, Lake Victoria",
        "target_audience": "domestic",
        "region": None,
        "is_featured": True,
    },
    {
        "slug": "kampala-city-cultural-tour",
        "title": "Kampala City & Cultural Tour",
        "description": (
            "Explore Uganda’s vibrant capital with visits to the Uganda Museum, Kasubi "
            "Tombs, local markets, and historical sites. Learn about Buganda culture, "
            "enjoy local cuisine, and see the city from different perspectives. Great "
            "for first-time visitors and locals wanting to rediscover Kampala."
        ),
        "price": None,
        "currency": "UGX",
        "price_basis": "per_person",
        "price_is_from": True,
        "duration_days": 1,
        "location": "Kampala",
        "target_audience": "domestic",
        "region": None,
        "is_featured": True,
    },
]


ITINERARY = [
    {
        "day": 1,
        "title": "Journey to Queen Elizabeth National Park",
        "description": (
            "Depart from Kampala or Entebbe and travel toward Queen Elizabeth National "
            "Park. Stop at the Uganda Equator in Kayabwe for photographs before "
            "continuing to Mbarara for lunch.\n\nProceed through western Uganda’s "
            "scenic countryside and the Bunyaruguru crater region. Arrive at the "
            "selected lodge, check in and relax before dinner."
        ),
        "meals": "Lunch and dinner",
        "accommodation": "",
    },
    {
        "day": 2,
        "title": "Kasenyi game drive and Kazinga Channel cruise",
        "description": (
            "Begin with an early morning game drive across the Kasenyi plains. Look out "
            "for elephants, buffaloes, Uganda kobs, lions, leopards and a variety of "
            "bird species. Wildlife sightings depend on natural conditions and cannot "
            "be guaranteed.\n\nReturn to the lodge for breakfast and lunch. In the "
            "afternoon, join a scheduled boat cruise along the Kazinga Channel and "
            "observe wildlife gathering near the water.\n\nReturn to the lodge for "
            "dinner and an overnight stay."
        ),
        "meals": "Breakfast, lunch and dinner",
        "accommodation": "",
    },
    {
        "day": 3,
        "title": "Optional forest experience and return journey",
        "description": (
            "After breakfast, enjoy a relaxed morning or take part in an optional "
            "chimpanzee-tracking experience in Kalinzu Forest Reserve.\n\nChimpanzee "
            "tracking must be arranged in advance and is subject to permit availability, "
            "forest regulations and final confirmation.\n\nBegin the return journey "
            "after the morning programme. Stop for lunch and continue directly to "
            "Kampala, Entebbe International Airport or another agreed destination."
        ),
        "meals": "Breakfast and lunch",
        "accommodation": "",
    },
]


def sync_site_content(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    Itinerary = apps.get_model("tours", "Itinerary")

    synced_tours = {}
    for record in TOURS:
        values = record.copy()
        slug = values.pop("slug")
        tour, _ = Tour.objects.update_or_create(slug=slug, defaults=values)
        synced_tours[slug] = tour

    queen_elizabeth = synced_tours["3-day-queen-elizabeth-safari"]
    for record in ITINERARY:
        values = record.copy()
        day = values.pop("day")
        Itinerary.objects.update_or_create(
            tour=queen_elizabeth,
            day=day,
            defaults=values,
        )


class Migration(migrations.Migration):
    dependencies = [("tours", "0010_itinerary_meals_accommodation")]

    operations = [migrations.RunPython(sync_site_content, migrations.RunPython.noop)]