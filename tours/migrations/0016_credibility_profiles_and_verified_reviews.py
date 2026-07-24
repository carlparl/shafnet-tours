from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0015_complete_and_expand_tour_catalogue"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompanyCredential",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text=(
                            "For example: Uganda Tourism Board operator licence."
                        ),
                        max_length=150,
                    ),
                ),
                (
                    "issuer",
                    models.CharField(
                        blank=True,
                        help_text=(
                            "Organisation that issued or maintains the credential."
                        ),
                        max_length=150,
                    ),
                ),
                (
                    "identifier",
                    models.CharField(
                        blank=True,
                        help_text=(
                            "Licence or membership number, if it is public."
                        ),
                        max_length=120,
                    ),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=240),
                ),
                (
                    "verification_url",
                    models.URLField(
                        help_text=(
                            "Public page where a traveller can verify this "
                            "credential."
                        )
                    ),
                ),
                (
                    "logo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="credentials/",
                    ),
                ),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "is_active",
                    models.BooleanField(
                        default=False,
                        help_text=(
                            "Activate only after the name, number and verification "
                            "link have been checked."
                        ),
                    ),
                ),
            ],
            options={"ordering": ["order", "name"]},
        ),
        migrations.CreateModel(
            name="TeamMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                ("role", models.CharField(max_length=120)),
                ("bio", models.TextField()),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="team/",
                    ),
                ),
                (
                    "qualifications",
                    models.CharField(
                        blank=True,
                        help_text=(
                            "Only include qualifications that can be supported."
                        ),
                        max_length=240,
                    ),
                ),
                (
                    "languages",
                    models.CharField(
                        blank=True,
                        help_text=(
                            "For example: English, Luganda and Runyankole."
                        ),
                        max_length=200,
                    ),
                ),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "is_active",
                    models.BooleanField(
                        default=False,
                        help_text=(
                            "Activate when the profile and photo are approved."
                        ),
                    ),
                ),
            ],
            options={"ordering": ["order", "name"]},
        ),
        migrations.AddField(
            model_name="testimonial",
            name="is_verified",
            field=models.BooleanField(
                default=False,
                help_text=(
                    "Enable only after checking that the source link belongs to "
                    "this review. Only verified reviews appear on the website."
                ),
            ),
        ),
        migrations.AddField(
            model_name="testimonial",
            name="source_name",
            field=models.CharField(
                blank=True,
                help_text=(
                    "For example: Google, Tripadvisor or SafariBookings."
                ),
                max_length=80,
            ),
        ),
        migrations.AddField(
            model_name="testimonial",
            name="source_url",
            field=models.URLField(
                blank=True,
                help_text="Link to the original public review.",
            ),
        ),
        migrations.AddField(
            model_name="testimonial",
            name="tour_name",
            field=models.CharField(
                blank=True,
                help_text=(
                    "Optional trip or itinerary connected to this review."
                ),
                max_length=180,
            ),
        ),
        migrations.AddField(
            model_name="testimonial",
            name="travel_date",
            field=models.DateField(
                blank=True,
                help_text="Optional month or date of travel.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="testimonial",
            name="rating",
            field=models.IntegerField(
                default=5,
                validators=[
                    MinValueValidator(1),
                    MaxValueValidator(5),
                ],
            ),
        ),
    ]
