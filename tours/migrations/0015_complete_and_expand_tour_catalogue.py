from django.db import migrations


STANDARD_EXCLUSIONS = """Flights unless expressly stated
Visa fees
Travel and medical insurance
Alcoholic and additional beverages
Personal telephone charges and laundry services
Optional activities and permits
Tips and gratuities
Personal expenses
Services not expressly stated as included"""


TOURS = [
    {
        "slug": "2-day-bwindi-gorilla-trekking",
        "description": "Track mountain gorillas in Bwindi Impenetrable National Park on a focused two-day journey. The experience includes forest-sector transfers, an official briefing and a guided trek. Permits, sector, accommodation and transport must be confirmed in advance.",
        "inclusions": "Ground transportation in a 4×4 safari vehicle\nOne night’s accommodation\nMeals specified in the itinerary\nProfessional driver-guide\nBwindi park entry and gorilla-tracking permit when stated in the final quote\nBottled drinking water",
        "exclusions": STANDARD_EXCLUSIONS,
        "optional_activities": "Community experience\nGuided birding\nAdditional forest nature walk",
        "days": [
            (1, "Journey to Bwindi", "Travel to the confirmed Bwindi trekking sector, with suitable stops along the way. Check in near the forest and receive preparation guidance for the following morning.", "Lunch and dinner", "Selected lodge near the confirmed Bwindi sector"),
            (2, "Gorilla-tracking experience", "Report for the official briefing before joining the guided forest trek. Trek duration and conditions vary. After the activity, continue to the agreed destination. Participation is subject to a valid permit and Uganda Wildlife Authority rules.", "Breakfast and packed lunch", ""),
        ],
    },
    {
        "slug": "entebbe-airport-transfer",
        "description": "A pre-arranged private transfer between Entebbe International Airport and Kampala, Entebbe or another confirmed nearby destination. Pickup details, passenger numbers, luggage requirements and the final drop-off point are confirmed before travel.",
        "inclusions": "Private vehicle for the confirmed route\nProfessional driver\nAirport pickup or drop-off assistance\nFuel and standard route costs",
        "exclusions": "Flights and visa fees\nAccommodation and meals\nExtra waiting time not included in the quote\nAdditional stops or route changes\nParking or access charges not stated in the quote\nPersonal expenses",
        "optional_activities": "Meet-and-greet assistance\nAdditional stop in Entebbe\nReturn transfer\nLarger vehicle for groups or extra luggage",
        "days": [(1, "Airport pickup and private transfer", "Meet your Shafnet representative at the confirmed pickup point and continue by private vehicle to the agreed destination. Flight, contact and drop-off details are checked before service.", "", "")],
    },
    {
        "slug": "5-day-ssese-islands-beach-escape",
        "description": "Slow down on Bugala Island in the Ssese archipelago, surrounded by Lake Victoria scenery. This five-day escape combines ferry travel, relaxed beach time and flexible island experiences, subject to ferry schedules, weather and local availability.",
        "inclusions": "Return ground and scheduled ferry transfers\nFour nights’ accommodation\nMeals specified in the itinerary\nLocal coordination\nActivities expressly confirmed in the final itinerary",
        "exclusions": STANDARD_EXCLUSIONS,
        "optional_activities": "Guided island walk\nCommunity experience\nCycling\nAdditional boat experience",
        "days": [
            (1, "Travel to Bugala Island", "Transfer to the ferry departure point and cross to Bugala Island according to the confirmed schedule. Continue to the selected accommodation and settle in.", "Dinner", "Selected island lodge"),
            (2, "Beach and island relaxation", "Enjoy a relaxed day by Lake Victoria, with time at the lodge or beach and any pre-arranged light activities.", "Breakfast and dinner", "Selected island lodge"),
            (3, "Island nature and community experience", "Join a confirmed guided island, nature or community experience and learn more about everyday island life.", "Breakfast and dinner", "Selected island lodge"),
            (4, "Leisure day", "Spend the day at your own pace or choose from available optional activities arranged through the tour team.", "Breakfast and dinner", "Selected island lodge"),
            (5, "Return journey", "Check out after breakfast, transfer to the ferry point and continue to the agreed mainland drop-off location.", "Breakfast", ""),
        ],
    },
    {
        "slug": "kampala-city-cultural-tour",
        "description": "Discover Kampala through a flexible selection of cultural, historical and community landmarks. The route is adjusted to opening hours, traffic, guest interests and the attractions confirmed in the final itinerary.",
        "inclusions": "Private local transportation\nProfessional guide\nEntry fees for attractions expressly listed in the final itinerary\nBottled drinking water",
        "exclusions": "Accommodation\nMeals unless stated\nUnlisted attraction fees\nShopping and personal expenses\nTips and gratuities",
        "optional_activities": "Local lunch experience\nCraft-market visit\nAdditional cultural site\nEvening city experience",
        "days": [(1, "Discover Kampala", "Meet your guide and visit the confirmed cultural and historical attractions around Kampala. Allow time for interpretation, photographs and an optional local meal before returning to the agreed drop-off point.", "Lunch when included in the final quote", "")],
    },
    {
        "slug": "3-day-sipi-falls-coffee-experience",
        "create": {"title": "3-Day Sipi Falls & Coffee Experience", "duration_days": 3, "location": "Sipi Falls, Kapchorwa", "target_audience": "domestic", "region": "eastern"},
        "description": "Explore the landscapes around Sipi Falls on a three-day eastern Uganda escape. Enjoy guided waterfall viewpoints, a locally arranged coffee experience and time in the highland scenery. Walking routes depend on weather and local conditions.",
        "inclusions": "Private ground transportation\nTwo nights’ accommodation\nMeals specified in the itinerary\nProfessional guide\nConfirmed waterfall and coffee experiences\nBottled drinking water",
        "exclusions": STANDARD_EXCLUSIONS,
        "optional_activities": "Birding experience\nCommunity visit\nAdditional scenic walk",
        "days": [
            (1, "Journey to Sipi Falls", "Travel east to Sipi, check in and enjoy the surrounding highland scenery as time permits.", "Lunch and dinner", "Selected lodge near Sipi Falls"),
            (2, "Waterfall and coffee experience", "Join a guided walk to confirmed Sipi viewpoints, followed by a locally arranged coffee experience. The route is adapted to weather and guest ability.", "Breakfast, lunch and dinner", "Selected lodge near Sipi Falls"),
            (3, "Scenic morning and return", "Enjoy a relaxed morning or short confirmed activity before returning to the agreed destination.", "Breakfast and lunch", ""),
        ],
    },
    {
        "slug": "3-day-lake-bunyonyi-retreat",
        "create": {"title": "3-Day Lake Bunyonyi Retreat", "duration_days": 3, "location": "Lake Bunyonyi, Kabale", "target_audience": "domestic", "region": "western"},
        "description": "Relax beside Lake Bunyonyi on a three-day retreat shaped around scenery, rest and gentle local experiences. Accommodation and activities are selected according to guest preferences, weather and availability.",
        "inclusions": "Private ground transportation\nTwo nights’ accommodation\nMeals specified in the itinerary\nLocal coordination\nConfirmed lake or community experience",
        "exclusions": STANDARD_EXCLUSIONS,
        "optional_activities": "Guided community experience\nBirding\nScenic boat experience\nAdditional island visit",
        "days": [
            (1, "Journey to Lake Bunyonyi", "Travel to Kabale and continue to the selected lakeside accommodation. Check in and enjoy the evening scenery.", "Lunch and dinner", "Selected lodge at Lake Bunyonyi"),
            (2, "Lake and community experience", "Enjoy a confirmed lake, island or community experience, with time to relax at the accommodation.", "Breakfast, lunch and dinner", "Selected lodge at Lake Bunyonyi"),
            (3, "Relaxed morning and return", "Have breakfast and enjoy a final view of the lake before beginning the return journey.", "Breakfast and lunch", ""),
        ],
    },
    {
        "slug": "2-day-lake-mburo-safari",
        "create": {"title": "2-Day Lake Mburo Safari", "duration_days": 2, "location": "Lake Mburo National Park", "target_audience": "domestic", "region": "western"},
        "description": "Take a compact wildlife break in Lake Mburo National Park, combining scenic travel with confirmed game-viewing activities. The programme is suitable for travellers seeking a shorter safari from Kampala or Entebbe.",
        "inclusions": "Private 4×4 ground transportation\nOne night’s accommodation\nMeals specified in the itinerary\nProfessional driver-guide\nPark entrance fees\nConfirmed game drive\nBottled drinking water",
        "exclusions": STANDARD_EXCLUSIONS,
        "optional_activities": "Guided nature walk\nBoat experience\nBirding\nCommunity experience",
        "days": [
            (1, "Travel and afternoon game viewing", "Travel to Lake Mburo National Park, enter the conservation area and enjoy a confirmed afternoon game drive before checking in.", "Lunch and dinner", "Selected lodge near Lake Mburo National Park"),
            (2, "Morning activity and return", "Join a scheduled morning game drive or other confirmed park activity, then begin the return journey to the agreed destination.", "Breakfast and lunch", ""),
        ],
    },
    {
        "slug": "2-day-jinja-nile-culture-escape",
        "create": {"title": "2-Day Jinja Nile & Culture Escape", "duration_days": 2, "location": "Jinja", "target_audience": "domestic", "region": "eastern"},
        "description": "Enjoy a two-day visit to Jinja combining Nile scenery, local heritage and a relaxed city experience. The programme avoids a rushed day trip and can be adjusted for families, groups or private travellers.",
        "inclusions": "Private ground transportation\nOne night’s accommodation\nMeals specified in the itinerary\nProfessional guide\nConfirmed Nile and cultural activities\nBottled drinking water",
        "exclusions": STANDARD_EXCLUSIONS,
        "optional_activities": "Additional Nile boat experience\nCraft-market visit\nCommunity experience\nAdditional city attraction",
        "days": [
            (1, "Journey to Jinja and Nile experience", "Travel to Jinja, visit the confirmed Nile attraction and enjoy a guided introduction to the city before checking in.", "Lunch and dinner", "Selected hotel in Jinja"),
            (2, "Jinja culture and return", "Visit selected cultural or historical attractions, allow time for lunch and return to the agreed destination.", "Breakfast and lunch", ""),
        ],
    },
]


def sync_catalogue(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    Itinerary = apps.get_model("tours", "Itinerary")
    for record in TOURS:
        create = record.get("create")
        defaults = {
            "description": record["description"],
            "inclusions": record["inclusions"],
            "exclusions": record["exclusions"],
            "optional_activities": record["optional_activities"],
        }
        if create:
            defaults.update(create)
            defaults.update({"price": None, "currency": "UGX" if create["target_audience"] == "domestic" else "USD", "price_basis": "per_person", "price_is_from": True, "is_featured": True})
            tour, _ = Tour.objects.update_or_create(slug=record["slug"], defaults=defaults)
        else:
            tour = Tour.objects.filter(slug=record["slug"]).first()
            if not tour:
                continue
            for field, value in defaults.items():
                setattr(tour, field, value)
            tour.save(update_fields=list(defaults))
        for day, title, description, meals, accommodation in record["days"]:
            Itinerary.objects.update_or_create(tour=tour, day=day, defaults={"title": title, "description": description, "meals": meals, "accommodation": accommodation})


class Migration(migrations.Migration):
    dependencies = [("tours", "0014_add_murchison_tour_content")]
    operations = [migrations.RunPython(sync_catalogue, migrations.RunPython.noop)]
