from django.db import migrations


INCLUSIONS = """Two nights’ accommodation in the selected category
Meals specified in the itinerary
Private ground transportation in a 4×4 safari vehicle
Services of an English-speaking professional driver-guide
Queen Elizabeth National Park entrance fees
Morning game drive across the Kasenyi plains
Scheduled Kazinga Channel boat cruise
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

OPTIONAL_ACTIVITIES = """Chimpanzee tracking in Kalinzu Forest Reserve
Guided birding experience
Community visit
Crater-lake exploration"""


def add_package_details(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    Tour.objects.filter(slug="3-day-queen-elizabeth-safari").update(
        inclusions=INCLUSIONS,
        exclusions=EXCLUSIONS,
        optional_activities=OPTIONAL_ACTIVITIES,
    )


class Migration(migrations.Migration):
    dependencies = [("tours", "0012_tour_package_details")]

    operations = [migrations.RunPython(add_package_details, migrations.RunPython.noop)]