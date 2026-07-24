from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0018_distinguish_safari_journey_styles"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactmessage",
            name="is_read",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="contactmessage",
            name="read_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
