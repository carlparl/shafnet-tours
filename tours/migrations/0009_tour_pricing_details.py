import django.core.validators
from django.db import migrations, models


def assign_existing_tour_currencies(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    Tour.objects.filter(target_audience="domestic").update(currency="UGX")
    Tour.objects.filter(target_audience="international").update(currency="USD")


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0008_destination_alter_tour_region"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tour",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text=(
                    "Enter the amount only. Select its currency and basis below."
                ),
                max_digits=10,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.AddField(
            model_name="tour",
            name="currency",
            field=models.CharField(
                choices=[
                    ("UGX", "Ugandan shillings (UGX)"),
                    ("USD", "US dollars (USD)"),
                ],
                default="USD",
                max_length=3,
            ),
        ),
        migrations.AddField(
            model_name="tour",
            name="price_basis",
            field=models.CharField(
                choices=[
                    ("per_person", "Per person"),
                    ("per_group", "Per group"),
                ],
                default="per_person",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="tour",
            name="price_is_from",
            field=models.BooleanField(
                default=True,
                verbose_name="Show as a starting price",
            ),
        ),
        migrations.RunPython(
            assign_existing_tour_currencies,
            migrations.RunPython.noop,
        ),
    ]
