from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("tours", "0009_tour_pricing_details")]

    operations = [
        migrations.AddField(
            model_name="itinerary",
            name="accommodation",
            field=models.CharField(blank=True, help_text="Optional overnight accommodation or lodge.", max_length=200),
        ),
        migrations.AddField(
            model_name="itinerary",
            name="meals",
            field=models.CharField(blank=True, help_text="Optional, for example: Breakfast, lunch and dinner.", max_length=150),
        ),
    ]
