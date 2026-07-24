from django.db import migrations, models


STANDARD_EXCLUSIONS = """International and domestic flights
Uganda visa fees
Travel and medical insurance
Alcoholic and additional beverages
Laundry, telephone charges and personal expenses
Optional activities and permits not confirmed in the final quotation
Tips and gratuities
Services not expressly stated as included"""


CATALOGUE_ORDER = {
    "3-day-queen-elizabeth-safari": 10,
    "4-day-murchison-falls-adventure": 20,
    "2-day-bwindi-gorilla-trekking": 30,
    "3-day-kibale-chimpanzee-experience": 40,
    "5-day-gorilla-and-queen-elizabeth-safari": 50,
    "5-day-kidepo-valley-wilderness-safari": 60,
    "7-day-western-uganda-wildlife-and-primates": 70,
    "10-day-uganda-grand-safari": 80,
    "entebbe-airport-transfer": 10,
    "kampala-city-cultural-tour": 20,
    "2-day-jinja-nile-culture-escape": 30,
    "2-day-lake-mburo-safari": 40,
    "3-day-sipi-falls-coffee-experience": 50,
    "3-day-lake-bunyonyi-retreat": 60,
    "5-day-ssese-islands-beach-escape": 70,
}


NEW_TOURS = [
    {
        "slug": "3-day-kibale-chimpanzee-experience",
        "title": "3-Day Kibale Chimpanzee Experience",
        "description": (
            "Explore Kibale National Park on a focused primate journey built "
            "around a professionally guided chimpanzee-tracking session. The "
            "programme includes time in the Fort Portal and Kibale area, with "
            "the final tracking time, permit and accommodation confirmed "
            "before travel. Wildlife sightings and trek duration depend on "
            "natural conditions."
        ),
        "inclusions": """Private ground transportation in a suitable safari vehicle
Two nights’ accommodation
Meals specified in the itinerary
Professional English-speaking driver-guide
Kibale National Park entry
Confirmed chimpanzee-tracking permit shown in the final quotation
Bottled drinking water
Applicable government taxes and levies""",
        "exclusions": STANDARD_EXCLUSIONS,
        "optional_activities": """Community-guided wetland walk
Fort Portal crater-lake experience
Additional birding or nature walk
Chimpanzee habituation experience instead of standard tracking, when available""",
        "duration_days": 3,
        "location": "Kibale National Park & Fort Portal",
        "region": "western",
        "display_order": 40,
        "days": [
            (
                1,
                "Journey to the Kibale region",
                "Depart from Kampala or Entebbe and travel west toward Fort "
                "Portal and the Kibale area. Stop for refreshments as agreed, "
                "check in at the selected accommodation and receive guidance "
                "for the following day’s forest activity.",
                "Lunch and dinner",
                "Selected lodge in the Kibale or Fort Portal area",
            ),
            (
                2,
                "Guided chimpanzee tracking",
                "Report to the confirmed visitor centre for registration and "
                "a ranger briefing before entering the forest for the "
                "scheduled chimpanzee-tracking session. Tracking time and "
                "sightings vary. Spend the remainder of the day at leisure or "
                "join a separately confirmed community or nature experience.",
                "Breakfast, lunch and dinner",
                "Selected lodge in the Kibale or Fort Portal area",
            ),
            (
                3,
                "Return to Kampala or Entebbe",
                "Have breakfast, check out and begin the return journey to "
                "Kampala, Entebbe or another agreed drop-off point.",
                "Breakfast and lunch",
                "",
            ),
        ],
    },
    {
        "slug": "5-day-kidepo-valley-wilderness-safari",
        "title": "5-Day Kidepo Valley Wilderness Safari",
        "description": (
            "Travel into northern Uganda for a road safari to Kidepo Valley "
            "National Park. The five-day structure breaks up the long journey "
            "and allows meaningful time for game viewing in the park. Routes, "
            "overnight stops and activities are confirmed according to road "
            "conditions and accommodation availability."
        ),
        "inclusions": """Private 4×4 ground transportation
Four nights’ accommodation
Meals specified in the itinerary
Professional English-speaking driver-guide
Kidepo Valley National Park entrance fees
Confirmed game drives
Bottled drinking water
Applicable government taxes and levies""",
        "exclusions": STANDARD_EXCLUSIONS,
        "optional_activities": """Community experience arranged with an approved local host
Additional birding experience
Scheduled or charter flight upgrade
Additional park activity confirmed before travel""",
        "duration_days": 5,
        "location": "Kidepo Valley National Park",
        "region": "northern",
        "display_order": 60,
        "days": [
            (
                1,
                "Travel north",
                "Leave Kampala or Entebbe early and travel north, stopping "
                "overnight in the Gulu or Kitgum area to make the road journey "
                "more comfortable.",
                "Lunch and dinner",
                "Selected hotel in Gulu or Kitgum",
            ),
            (
                2,
                "Continue to Kidepo Valley National Park",
                "Continue to Kidepo, enter the protected area and check in at "
                "the selected accommodation. Join an afternoon game drive if "
                "arrival time and park conditions allow.",
                "Breakfast, lunch and dinner",
                "Selected lodge near Kidepo Valley National Park",
            ),
            (
                3,
                "Full-day Kidepo wildlife experience",
                "Explore the park through scheduled morning and afternoon game "
                "drives. The guide selects suitable routes according to current "
                "wildlife movement, weather and park guidance.",
                "Breakfast, lunch and dinner",
                "Selected lodge near Kidepo Valley National Park",
            ),
            (
                4,
                "Final park activity and return south",
                "Enjoy a final confirmed park activity before checking out and "
                "travelling back toward Kitgum or Gulu for the overnight stop.",
                "Breakfast, lunch and dinner",
                "Selected hotel in Kitgum or Gulu",
            ),
            (
                5,
                "Return to Kampala or Entebbe",
                "Complete the road journey to the agreed Kampala or Entebbe "
                "drop-off point, with suitable rest stops along the way.",
                "Breakfast and lunch",
                "",
            ),
        ],
    },
    {
        "slug": "5-day-gorilla-and-queen-elizabeth-safari",
        "title": "5-Day Gorilla & Queen Elizabeth Safari",
        "description": (
            "Combine savannah wildlife in Queen Elizabeth National Park with "
            "a permitted mountain-gorilla trek in Bwindi Impenetrable National "
            "Park. The route includes game viewing, a confirmed Kazinga "
            "Channel boat cruise and forest-sector transfers. Gorilla permits "
            "and the assigned trekking sector must be secured in advance."
        ),
        "inclusions": """Private 4×4 ground transportation
Four nights’ accommodation
Meals specified in the itinerary
Professional English-speaking driver-guide
Queen Elizabeth and Bwindi park entrance fees
Confirmed game drive and Kazinga Channel boat cruise
Confirmed gorilla-tracking permit shown in the final quotation
Bottled drinking water
Applicable government taxes and levies""",
        "exclusions": STANDARD_EXCLUSIONS,
        "optional_activities": """Community experience near Bwindi
Additional birding
Crater-lake experience
Additional game drive where timing permits""",
        "duration_days": 5,
        "location": "Queen Elizabeth National Park & Bwindi",
        "region": "western",
        "display_order": 50,
        "days": [
            (
                1,
                "Journey to Queen Elizabeth National Park",
                "Travel west from Kampala or Entebbe to Queen Elizabeth "
                "National Park, stopping as agreed before checking in near the "
                "park.",
                "Lunch and dinner",
                "Selected lodge near Queen Elizabeth National Park",
            ),
            (
                2,
                "Game drive and Kazinga Channel boat cruise",
                "Join a morning game drive followed by the confirmed afternoon "
                "boat cruise on the Kazinga Channel. Wildlife sightings remain "
                "subject to natural conditions.",
                "Breakfast, lunch and dinner",
                "Selected lodge near Queen Elizabeth National Park",
            ),
            (
                3,
                "Transfer to the confirmed Bwindi sector",
                "Check out and travel toward the Bwindi trekking sector shown "
                "on the permit. Arrive with time to prepare for the following "
                "morning’s forest activity.",
                "Breakfast, lunch and dinner",
                "Selected lodge near the confirmed Bwindi sector",
            ),
            (
                4,
                "Mountain-gorilla tracking",
                "Attend the official briefing and join the ranger-guided trek "
                "for the habituated gorilla family assigned to the permit. "
                "Trek duration and terrain vary, and participation remains "
                "subject to Uganda Wildlife Authority rules.",
                "Breakfast, packed lunch and dinner",
                "Selected lodge near the confirmed Bwindi sector",
            ),
            (
                5,
                "Return journey",
                "Check out after breakfast and return to Kampala, Entebbe or "
                "another agreed destination, with suitable stops en route.",
                "Breakfast and lunch",
                "",
            ),
        ],
    },
    {
        "slug": "7-day-western-uganda-wildlife-and-primates",
        "title": "7-Day Western Uganda Wildlife & Primates",
        "description": (
            "Connect three of western Uganda’s leading protected areas in one "
            "carefully paced route: Kibale for chimpanzee tracking, Queen "
            "Elizabeth for savannah wildlife and the Kazinga Channel, and "
            "Bwindi for permitted mountain-gorilla tracking. Both primate "
            "permits and the final route must be confirmed before travel."
        ),
        "inclusions": """Private 4×4 ground transportation
Six nights’ accommodation
Meals specified in the itinerary
Professional English-speaking driver-guide
Park entrance fees for confirmed protected areas
Confirmed chimpanzee- and gorilla-tracking permits shown in the final quotation
Confirmed game drive and Kazinga Channel boat cruise
Bottled drinking water
Applicable government taxes and levies""",
        "exclusions": STANDARD_EXCLUSIONS,
        "optional_activities": """Community-guided wetland walk
Crater-lake experience
Community experience near Bwindi
Additional birding or game-viewing activity""",
        "duration_days": 7,
        "location": "Kibale, Queen Elizabeth & Bwindi",
        "region": "western",
        "display_order": 70,
        "days": [
            (
                1,
                "Kampala or Entebbe to Kibale",
                "Travel west to the Kibale and Fort Portal area and check in "
                "for two nights.",
                "Lunch and dinner",
                "Selected lodge in the Kibale or Fort Portal area",
            ),
            (
                2,
                "Chimpanzee tracking",
                "Attend the ranger briefing and join the confirmed guided "
                "chimpanzee-tracking session. The remaining time is kept "
                "flexible for rest or a separately arranged local experience.",
                "Breakfast, lunch and dinner",
                "Selected lodge in the Kibale or Fort Portal area",
            ),
            (
                3,
                "Transfer to Queen Elizabeth National Park",
                "Travel south toward Queen Elizabeth National Park, with a "
                "scenic or crater-area stop when practical, then check in near "
                "the park.",
                "Breakfast, lunch and dinner",
                "Selected lodge near Queen Elizabeth National Park",
            ),
            (
                4,
                "Savannah game viewing and Kazinga Channel",
                "Join a morning game drive and the confirmed afternoon boat "
                "cruise. The exact sequence may change with park schedules.",
                "Breakfast, lunch and dinner",
                "Selected lodge near Queen Elizabeth National Park",
            ),
            (
                5,
                "Continue to Bwindi",
                "Travel to the Bwindi sector allocated on the gorilla permit "
                "and prepare for the following day’s trek.",
                "Breakfast, lunch and dinner",
                "Selected lodge near the confirmed Bwindi sector",
            ),
            (
                6,
                "Mountain-gorilla tracking",
                "Join the official briefing and ranger-guided forest trek. "
                "Trek duration, terrain and sightings depend on natural "
                "conditions and the assigned gorilla family.",
                "Breakfast, packed lunch and dinner",
                "Selected lodge near the confirmed Bwindi sector",
            ),
            (
                7,
                "Return to Kampala or Entebbe",
                "Check out and complete the return journey to the agreed "
                "drop-off point.",
                "Breakfast and lunch",
                "",
            ),
        ],
    },
    {
        "slug": "10-day-uganda-grand-safari",
        "title": "10-Day Uganda Grand Safari",
        "description": (
            "Experience a broad Uganda circuit combining Murchison Falls, "
            "Kibale, Queen Elizabeth, Bwindi and Lake Mburo. The route balances "
            "savannah game viewing, boat experiences and permitted primate "
            "tracking with practical travel days. All permits, park activities "
            "and accommodation are confirmed in the final itinerary."
        ),
        "inclusions": """Private 4×4 ground transportation
Nine nights’ accommodation
Meals specified in the itinerary
Professional English-speaking driver-guide
Park entrance fees for confirmed protected areas
Confirmed chimpanzee- and gorilla-tracking permits shown in the final quotation
Confirmed game drives and scheduled boat experiences
Bottled drinking water
Applicable government taxes and levies""",
        "exclusions": STANDARD_EXCLUSIONS,
        "optional_activities": """Rhino tracking at Ziwa when expressly added to the final route
Community-guided wetland walk
Community experience near Bwindi
Additional nature walk, birding or game-viewing activity""",
        "duration_days": 10,
        "location": "Murchison Falls, Kibale, Queen Elizabeth, Bwindi & Lake Mburo",
        "region": None,
        "display_order": 80,
        "days": [
            (
                1,
                "Journey to Murchison Falls",
                "Travel north from Kampala or Entebbe to the Murchison Falls "
                "region, with agreed stops before checking in.",
                "Lunch and dinner",
                "Selected lodge near Murchison Falls National Park",
            ),
            (
                2,
                "Murchison game drive and Nile experience",
                "Join a morning game drive and the confirmed scheduled boat "
                "experience on the Nile, subject to park operations and "
                "weather.",
                "Breakfast, lunch and dinner",
                "Selected lodge near Murchison Falls National Park",
            ),
            (
                3,
                "Transfer to Kibale",
                "Travel south-west toward the Kibale and Fort Portal area and "
                "check in for the night.",
                "Breakfast, lunch and dinner",
                "Selected lodge in the Kibale or Fort Portal area",
            ),
            (
                4,
                "Kibale chimpanzee tracking",
                "Attend the ranger briefing and join the confirmed guided "
                "chimpanzee-tracking session.",
                "Breakfast, lunch and dinner",
                "Selected lodge in the Kibale or Fort Portal area",
            ),
            (
                5,
                "Continue to Queen Elizabeth National Park",
                "Travel to Queen Elizabeth National Park, with a scenic stop "
                "where practical, and check in near the park.",
                "Breakfast, lunch and dinner",
                "Selected lodge near Queen Elizabeth National Park",
            ),
            (
                6,
                "Queen Elizabeth game drive and Kazinga Channel",
                "Join a morning game drive followed by the confirmed Kazinga "
                "Channel boat cruise.",
                "Breakfast, lunch and dinner",
                "Selected lodge near Queen Elizabeth National Park",
            ),
            (
                7,
                "Transfer to Bwindi",
                "Continue to the Bwindi sector assigned on the gorilla permit "
                "and prepare for the forest trek.",
                "Breakfast, lunch and dinner",
                "Selected lodge near the confirmed Bwindi sector",
            ),
            (
                8,
                "Mountain-gorilla tracking",
                "Join the official briefing and ranger-guided gorilla trek, "
                "subject to the permit and Uganda Wildlife Authority rules.",
                "Breakfast, packed lunch and dinner",
                "Selected lodge near the confirmed Bwindi sector",
            ),
            (
                9,
                "Bwindi to Lake Mburo",
                "Travel to the Lake Mburo area and join a confirmed afternoon "
                "activity if time and park schedules allow.",
                "Breakfast, lunch and dinner",
                "Selected lodge near Lake Mburo National Park",
            ),
            (
                10,
                "Final activity and return",
                "Enjoy the confirmed morning activity, check out and return to "
                "Kampala or Entebbe.",
                "Breakfast and lunch",
                "",
            ),
        ],
    },
]


def expand_catalogue(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    Itinerary = apps.get_model("tours", "Itinerary")

    for slug, display_order in CATALOGUE_ORDER.items():
        Tour.objects.filter(slug=slug).update(
            display_order=display_order,
            is_active=True,
        )

    for record in NEW_TOURS:
        defaults = {
            "title": record["title"],
            "description": record["description"],
            "inclusions": record["inclusions"],
            "exclusions": record["exclusions"],
            "optional_activities": record["optional_activities"],
            "price": None,
            "currency": "USD",
            "price_basis": "per_person",
            "price_is_from": True,
            "duration_days": record["duration_days"],
            "location": record["location"],
            "target_audience": "international",
            "region": record["region"],
            "is_featured": False,
            "is_active": True,
            "display_order": record["display_order"],
        }
        tour, _created = Tour.objects.update_or_create(
            slug=record["slug"],
            defaults=defaults,
        )

        for day, title, description, meals, accommodation in record["days"]:
            Itinerary.objects.update_or_create(
                tour=tour,
                day=day,
                defaults={
                    "title": title,
                    "description": description,
                    "meals": meals,
                    "accommodation": accommodation,
                },
            )


def remove_added_tours(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    Tour.objects.filter(
        slug__in=[record["slug"] for record in NEW_TOURS]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0016_credibility_profiles_and_verified_reviews"),
    ]

    operations = [
        migrations.AddField(
            model_name="companycredential",
            name="valid_until",
            field=models.DateField(
                blank=True,
                help_text=(
                    "Optional expiry or renewal date shown on the credential."
                ),
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="tour",
            name="display_order",
            field=models.PositiveIntegerField(
                default=0,
                help_text="Lower numbers appear first within each catalogue.",
            ),
        ),
        migrations.AddField(
            model_name="tour",
            name="is_active",
            field=models.BooleanField(
                default=True,
                help_text=(
                    "Inactive tours are hidden from listings, search engines "
                    "and detail pages."
                ),
            ),
        ),
        migrations.AlterModelOptions(
            name="tour",
            options={"ordering": ["display_order", "title"]},
        ),
        migrations.RunPython(expand_catalogue, remove_added_tours),
    ]
