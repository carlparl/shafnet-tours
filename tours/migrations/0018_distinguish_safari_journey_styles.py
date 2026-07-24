from django.db import migrations, models


SAFARI_POSITIONING = {
    "3-day-queen-elizabeth-safari": {
        "title": "3-Day Queen Elizabeth Wildlife Safari",
        "journey_style": "focused",
        "best_for": (
            "First-time safari travellers seeking game viewing and a Kazinga "
            "Channel boat cruise in one national park."
        ),
    },
    "4-day-murchison-falls-adventure": {
        "title": "4-Day Murchison Falls & Nile Safari",
        "journey_style": "focused",
        "best_for": (
            "Travellers prioritising Murchison Falls, Nile scenery and "
            "savannah game viewing."
        ),
    },
    "3-day-kibale-chimpanzee-experience": {
        "title": "3-Day Kibale Chimpanzee Tracking",
        "journey_style": "focused",
        "best_for": (
            "Primate enthusiasts whose main priority is a guided chimpanzee-"
            "tracking experience."
        ),
    },
    "5-day-gorilla-and-queen-elizabeth-safari": {
        "title": "5-Day Queen Elizabeth & Bwindi Safari",
        "journey_style": "combo",
        "best_for": (
            "Travellers wanting one savannah park and one gorilla trek in a "
            "shorter two-park combination."
        ),
    },
    "5-day-kidepo-valley-wilderness-safari": {
        "title": "5-Day Kidepo Valley Wilderness Safari",
        "journey_style": "focused",
        "best_for": (
            "Travellers seeking a remote northern-Uganda wilderness safari "
            "with road travel broken into practical stages."
        ),
    },
    "7-day-western-uganda-wildlife-and-primates": {
        "title": "7-Day Western Uganda Primate Circuit",
        "journey_style": "circuit",
        "best_for": (
            "Primate-focused travellers combining chimpanzees, gorillas and "
            "Queen Elizabeth wildlife."
        ),
    },
    "10-day-uganda-grand-safari": {
        "title": "10-Day Uganda Grand Wildlife Circuit",
        "journey_style": "circuit",
        "best_for": (
            "Travellers wanting Shafnet’s broadest multi-park route with "
            "wildlife, boat experiences and primate tracking."
        ),
    },
}


DOMESTIC_POSITIONING = {
    "entebbe-airport-transfer": (
        "transfer",
        "Travellers needing a pre-arranged private airport pickup or drop-off.",
    ),
    "kampala-city-cultural-tour": (
        "day_trip",
        "Visitors wanting a flexible introduction to Kampala in one day.",
    ),
    "2-day-jinja-nile-culture-escape": (
        "short_escape",
        "Couples, families or groups seeking a relaxed overnight Jinja visit.",
    ),
    "2-day-lake-mburo-safari": (
        "short_escape",
        "Residents and short-stay visitors wanting a compact wildlife break.",
    ),
    "3-day-sipi-falls-coffee-experience": (
        "short_escape",
        "Active travellers interested in waterfalls, highland scenery and coffee.",
    ),
    "3-day-lake-bunyonyi-retreat": (
        "short_escape",
        "Travellers prioritising rest, lake scenery and gentle local experiences.",
    ),
    "5-day-ssese-islands-beach-escape": (
        "short_escape",
        "Travellers seeking a slower Lake Victoria island holiday.",
    ),
}


BWINDI_DESCRIPTION = (
    "Make mountain-gorilla tracking the centre of a practical three-day "
    "Bwindi journey. Day one is reserved for the long transfer to the "
    "confirmed forest sector, day two for the official briefing and guided "
    "trek, and day three for the return journey. The permit, trekking sector, "
    "accommodation and transport must be confirmed in advance."
)

BWINDI_INCLUSIONS = """Private ground transportation in a suitable safari vehicle
Two nights’ accommodation
Meals specified in the itinerary
Professional English-speaking driver-guide
Bwindi park entry
Confirmed gorilla-tracking permit shown in the final quotation
Bottled drinking water
Applicable government taxes and levies"""

BWINDI_EXCLUSIONS = """International and domestic flights
Uganda visa fees
Travel and medical insurance
Alcoholic and additional beverages
Laundry, telephone charges and personal expenses
Optional activities and permits not confirmed in the final quotation
Tips and gratuities
Services not expressly stated as included"""

BWINDI_DAYS = [
    (
        1,
        "Journey to the confirmed Bwindi sector",
        "Depart from Kampala or Entebbe and travel to the Bwindi trekking "
        "sector assigned on the permit. Take suitable rest stops, check in "
        "near the forest and receive preparation guidance for the trek.",
        "Lunch and dinner",
        "Selected lodge near the confirmed Bwindi sector",
    ),
    (
        2,
        "Mountain-gorilla tracking",
        "Attend the official briefing and join the ranger-guided forest trek "
        "for the habituated gorilla family assigned to the permit. Trek "
        "duration and terrain vary. Return to the lodge after the activity.",
        "Breakfast, packed lunch and dinner",
        "Selected lodge near the confirmed Bwindi sector",
    ),
    (
        3,
        "Return to Kampala or Entebbe",
        "Check out after breakfast and begin the return journey to Kampala, "
        "Entebbe or another agreed drop-off point.",
        "Breakfast and lunch",
        "",
    ),
]

ORIGINAL_BWINDI_DESCRIPTION = (
    "Track mountain gorillas in Bwindi Impenetrable National Park on a "
    "focused two-day journey. The experience includes forest-sector "
    "transfers, an official briefing and a guided trek. Permits, sector, "
    "accommodation and transport must be confirmed in advance."
)

ORIGINAL_BWINDI_INCLUSIONS = """Ground transportation in a 4×4 safari vehicle
One night’s accommodation
Meals specified in the itinerary
Professional driver-guide
Bwindi park entry and gorilla-tracking permit when stated in the final quote
Bottled drinking water"""

ORIGINAL_BWINDI_EXCLUSIONS = """Flights unless expressly stated
Visa fees
Travel and medical insurance
Alcoholic and additional beverages
Personal telephone charges and laundry services
Optional activities and permits
Tips and gratuities
Personal expenses
Services not expressly stated as included"""


ORIGINAL_TITLES = {
    "3-day-queen-elizabeth-safari": "3-Day Queen Elizabeth Safari",
    "4-day-murchison-falls-adventure": "4-Day Murchison Falls Adventure",
    "3-day-kibale-chimpanzee-experience": "3-Day Kibale Chimpanzee Experience",
    "5-day-gorilla-and-queen-elizabeth-safari": (
        "5-Day Gorilla & Queen Elizabeth Safari"
    ),
    "5-day-kidepo-valley-wilderness-safari": (
        "5-Day Kidepo Valley Wilderness Safari"
    ),
    "7-day-western-uganda-wildlife-and-primates": (
        "7-Day Western Uganda Wildlife & Primates"
    ),
    "10-day-uganda-grand-safari": "10-Day Uganda Grand Safari",
}


def distinguish_catalogue(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    Itinerary = apps.get_model("tours", "Itinerary")

    for slug, values in SAFARI_POSITIONING.items():
        Tour.objects.filter(slug=slug).update(**values)

    for slug, (journey_style, best_for) in DOMESTIC_POSITIONING.items():
        Tour.objects.filter(slug=slug).update(
            journey_style=journey_style,
            best_for=best_for,
        )

    bwindi = Tour.objects.filter(
        slug="2-day-bwindi-gorilla-trekking"
    ).first()
    if not bwindi:
        return

    bwindi.slug = "3-day-bwindi-gorilla-trekking"
    bwindi.title = "3-Day Bwindi Gorilla Trekking"
    bwindi.description = BWINDI_DESCRIPTION
    bwindi.inclusions = BWINDI_INCLUSIONS
    bwindi.exclusions = BWINDI_EXCLUSIONS
    bwindi.duration_days = 3
    bwindi.journey_style = "focused"
    bwindi.best_for = (
        "Travellers whose main priority is one permitted mountain-gorilla "
        "tracking experience."
    )
    bwindi.save(
        update_fields=[
            "slug",
            "title",
            "description",
            "inclusions",
            "exclusions",
            "duration_days",
            "journey_style",
            "best_for",
        ]
    )

    Itinerary.objects.filter(tour=bwindi).delete()
    for day, title, description, meals, accommodation in BWINDI_DAYS:
        Itinerary.objects.create(
            tour=bwindi,
            day=day,
            title=title,
            description=description,
            meals=meals,
            accommodation=accommodation,
        )


def restore_catalogue(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    Itinerary = apps.get_model("tours", "Itinerary")

    for slug, title in ORIGINAL_TITLES.items():
        Tour.objects.filter(slug=slug).update(title=title)

    bwindi = Tour.objects.filter(
        slug="3-day-bwindi-gorilla-trekking"
    ).first()
    if not bwindi:
        return

    bwindi.slug = "2-day-bwindi-gorilla-trekking"
    bwindi.title = "2-Day Bwindi Gorilla Trekking"
    bwindi.description = ORIGINAL_BWINDI_DESCRIPTION
    bwindi.inclusions = ORIGINAL_BWINDI_INCLUSIONS
    bwindi.exclusions = ORIGINAL_BWINDI_EXCLUSIONS
    bwindi.duration_days = 2
    bwindi.save(
        update_fields=[
            "slug",
            "title",
            "description",
            "inclusions",
            "exclusions",
            "duration_days",
        ]
    )

    Itinerary.objects.filter(tour=bwindi).delete()
    Itinerary.objects.create(
        tour=bwindi,
        day=1,
        title="Journey to Bwindi",
        description=(
            "Travel to the confirmed Bwindi trekking sector, with suitable "
            "stops along the way. Check in near the forest and receive "
            "preparation guidance for the following morning."
        ),
        meals="Lunch and dinner",
        accommodation="Selected lodge near the confirmed Bwindi sector",
    )
    Itinerary.objects.create(
        tour=bwindi,
        day=2,
        title="Gorilla-tracking experience",
        description=(
            "Report for the official briefing before joining the guided "
            "forest trek. After the activity, continue to the agreed "
            "destination."
        ),
        meals="Breakfast and packed lunch",
        accommodation="",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0017_expand_and_manage_tour_catalogue"),
    ]

    operations = [
        migrations.AddField(
            model_name="tour",
            name="best_for",
            field=models.CharField(
                blank=True,
                help_text=(
                    "A factual one-sentence guide to the traveller this tour suits."
                ),
                max_length=220,
            ),
        ),
        migrations.AddField(
            model_name="tour",
            name="journey_style",
            field=models.CharField(
                blank=True,
                choices=[
                    ("transfer", "Transfer service"),
                    ("day_trip", "Day experience"),
                    ("short_escape", "Short escape"),
                    ("focused", "Focused safari"),
                    ("combo", "Two-park combination"),
                    ("circuit", "Multi-park circuit"),
                ],
                help_text=(
                    "Explains how this package differs from similar tours."
                ),
                max_length=20,
            ),
        ),
        migrations.RunPython(distinguish_catalogue, restore_catalogue),
    ]
