from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("tours", "0011_sync_local_site_content")]

    operations = [
        migrations.AddField(
            model_name="tour",
            name="exclusions",
            field=models.TextField(blank=True, help_text="Enter one excluded service per line."),
        ),
        migrations.AddField(
            model_name="tour",
            name="inclusions",
            field=models.TextField(blank=True, help_text="Enter one included service per line."),
        ),
        migrations.AddField(
            model_name="tour",
            name="optional_activities",
            field=models.TextField(blank=True, help_text="Enter one optional activity per line."),
        ),
    ]
