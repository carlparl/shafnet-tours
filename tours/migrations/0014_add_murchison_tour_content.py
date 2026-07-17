from django.db import migrations


DESCRIPTION = """Experience Murchison Falls National Park on a four-day safari through Uganda’s largest protected conservation area. Explore the savannah on guided game drives, travel along the Nile on a scheduled boat cruise, and visit an approved viewpoint near the falls.

The itinerary combines wildlife viewing, river scenery and time to appreciate the park’s varied landscapes. Activities, accommodation and schedules remain subject to availability, weather, park regulations and final confirmation."""

INCLUSIONS = """Three nights’ accommodation in the selected category
Meals specified in the itinerary
Private ground transportation in a 4×4 safari vehicle
Services of an English-speaking professional driver-guide
Murchison Falls National Park entrance fees
Scheduled game drives described in the itinerary
Scheduled Nile boat cruise
Visit to an approved Murchison Falls viewpoint
Bottled drinking water during the safari
Applicable government taxes and levies"""

EXCLUSIONS = """International and domestic flights
Uganda visa fees
Travel and medical insurance
Alcoholic and additional beverages
Personal telephone charges
Laundry services
Optional activities and permits
Tips and gratuities
Personal expenses
Services not expressly stated as included"""

OPTIONAL_ACTIVITIES = """Guided nature walk
Additional birding experience
Community visit
Additional game drive"""

ITINERARY = [
    {
        "day": 1,
        "title": "Journey to Murchison Falls National Park",
        "description": """Depart from Kampala or Entebbe and travel north toward Murchison Falls National Park. Take suitable rest and refreshment stops during the journey.

Continue to the selected lodge near the park, check in and relax. Depending on arrival time and the confirmed programme, enjoy the surrounding scenery before dinner.""",
        "meals": "Lunch and dinner",
        "accommodation": "Selected lodge near Murchison Falls National Park",
    },
    {
        "day": 2,
        "title": "Morning game drive and Nile boat cruise",
        "description": """Begin with an early morning guided game drive through the park’s savannah areas. Look out for elephants, giraffes, buffaloes, antelopes, lions and a variety of bird species. Wildlife sightings depend on natural conditions and cannot be guaranteed.

Return to the lodge for breakfast and lunch. In the afternoon, join a scheduled boat cruise along the Nile toward Murchison Falls and observe wildlife along the riverbanks.

Return to the lodge for dinner and an overnight stay.""",
        "meals": "Breakfast, lunch and dinner",
        "accommodation": "Selected lodge near Murchison Falls National Park",
    },
    {
        "day": 3,
        "title": "Explore the falls and surrounding landscapes",
        "description": """After breakfast, continue exploring Murchison Falls National Park through a scheduled game drive, guided nature experience or another confirmed park activity.

Visit an approved viewpoint near Murchison Falls and take in the scenery as the Nile passes through the narrow gorge. The final programme will depend on park guidance, weather and activity availability.

Return to the lodge for dinner and an overnight stay.""",
        "meals": "Breakfast, lunch and dinner",
        "accommodation": "Selected lodge near Murchison Falls National Park",
    },
    {
        "day": 4,
        "title": "Return journey to Kampala or Entebbe",
        "description": """Enjoy breakfast at the lodge before checking out and beginning the return journey.

Take planned refreshment stops along the way and continue to Kampala, Entebbe International Airport or another agreed destination. The final arrival time will depend on traffic and the selected drop-off point.""",
        "meals": "Breakfast and lunch",
        "accommodation": "",
    },
]


def add_murchison_content(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    Itinerary = apps.get_model("tours", "Itinerary")
    tour = Tour.objects.filter(slug="4-day-murchison-falls-adventure").first()
    if tour is None:
        return

    tour.description = DESCRIPTION
    tour.inclusions = INCLUSIONS
    tour.exclusions = EXCLUSIONS
    tour.optional_activities = OPTIONAL_ACTIVITIES
    tour.save(update_fields=["description", "inclusions", "exclusions", "optional_activities"])

    for record in ITINERARY:
        values = record.copy()
        day = values.pop("day")
        Itinerary.objects.update_or_create(tour=tour, day=day, defaults=values)


class Migration(migrations.Migration):
    dependencies = [("tours", "0013_add_queen_elizabeth_package_details")]

    operations = [migrations.RunPython(add_murchison_content, migrations.RunPython.noop)]