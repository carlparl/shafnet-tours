from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.text import slugify


class Tour(models.Model):
    AUDIENCE_CHOICES = [
        ("domestic", "Domestic Tours"),
        ("international", "International Safaris"),
    ]

    REGION_CHOICES = [
        ("central", "Central Uganda"),
        ("western", "Western Uganda"),
        ("northern", "Northern Uganda"),
        ("eastern", "Eastern Uganda"),
    ]

    CURRENCY_CHOICES = [
        ("UGX", "Ugandan shillings (UGX)"),
        ("USD", "US dollars (USD)"),
    ]

    PRICE_BASIS_CHOICES = [
        ("per_person", "Per person"),
        ("per_group", "Per group"),
    ]

    JOURNEY_STYLE_CHOICES = [
        ("transfer", "Transfer service"),
        ("day_trip", "Day experience"),
        ("short_escape", "Short escape"),
        ("focused", "Focused safari"),
        ("combo", "Two-park combination"),
        ("circuit", "Multi-park circuit"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    inclusions = models.TextField(
        blank=True,
        help_text="Enter one included service per line.",
    )
    exclusions = models.TextField(
        blank=True,
        help_text="Enter one excluded service per line.",
    )
    optional_activities = models.TextField(
        blank=True,
        help_text="Enter one optional activity per line.",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Enter the amount only. Select its currency and basis below.",
        validators=[MinValueValidator(0)],
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default="USD",
    )
    price_basis = models.CharField(
        max_length=20,
        choices=PRICE_BASIS_CHOICES,
        default="per_person",
    )
    price_is_from = models.BooleanField(
        default=True,
        verbose_name="Show as a starting price",
    )
    duration_days = models.PositiveIntegerField()
    location = models.CharField(max_length=200)
    target_audience = models.CharField(
        max_length=20,
        choices=AUDIENCE_CHOICES,
        default="international",
    )
    region = models.CharField(
        max_length=20,
        choices=REGION_CHOICES,
        blank=True,
        null=True,
    )
    journey_style = models.CharField(
        max_length=20,
        choices=JOURNEY_STYLE_CHOICES,
        blank=True,
        help_text="Explains how this package differs from similar tours.",
    )
    best_for = models.CharField(
        max_length=220,
        blank=True,
        help_text="A factual one-sentence guide to the traveller this tour suits.",
    )
    image = models.ImageField(upload_to="tours/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive tours are hidden from listings, search engines and detail pages.",
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first within each catalogue.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "tour"
            candidate = base_slug
            suffix = 2
            queryset = type(self).objects.exclude(pk=self.pk)

            while queryset.filter(slug=candidate).exists():
                candidate = f"{base_slug}-{suffix}"
                suffix += 1

            self.slug = candidate

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tour_detail", kwargs={"slug": self.slug})

    @staticmethod
    def _clean_list(value):
        return [item.strip() for item in value.splitlines() if item.strip()]

    @property
    def inclusion_items(self):
        return self._clean_list(self.inclusions)

    @property
    def exclusion_items(self):
        return self._clean_list(self.exclusions)

    @property
    def optional_activity_items(self):
        return self._clean_list(self.optional_activities)

    @property
    def formatted_price(self):
        if self.price is None:
            return ""

        if self.price == self.price.to_integral_value():
            amount = f"{self.price:,.0f}"
        else:
            amount = f"{self.price:,.2f}"
        return f"{self.currency} {amount}"

    @property
    def price_summary(self):
        if self.price is None:
            return "Price on request"

        prefix = "From " if self.price_is_from else ""
        basis = self.get_price_basis_display().lower()
        return f"{prefix}{self.formatted_price} {basis}"

    def __str__(self):
        return self.title


class Itinerary(models.Model):
    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="itineraries",
    )
    day = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    meals = models.CharField(max_length=150, blank=True, help_text="Optional, for example: Breakfast, lunch and dinner.")
    accommodation = models.CharField(max_length=200, blank=True, help_text="Optional overnight accommodation or lodge.")

    class Meta:
        ordering = ["day"]

    def __str__(self):
        return f"Day {self.day} - {self.title}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    number_of_people = models.PositiveIntegerField(default=1)
    preferred_date = models.DateField(null=True, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.tour.title}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    tour_name = models.CharField(
        max_length=180,
        blank=True,
        help_text="Optional trip or itinerary connected to this review.",
    )
    travel_date = models.DateField(
        blank=True,
        null=True,
        help_text="Optional month or date of travel.",
    )
    source_name = models.CharField(
        max_length=80,
        blank=True,
        help_text="For example: Google, Tripadvisor or SafariBookings.",
    )
    source_url = models.URLField(
        blank=True,
        help_text="Link to the original public review.",
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=(
            "Enable only after checking that the source link belongs to this "
            "review. Only verified reviews appear on the website."
        ),
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.rating} stars"

    @property
    def rating_stars(self):
        return "★" * self.rating

    @property
    def rating_empty_stars(self):
        return "☆" * (5 - self.rating)


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    bio = models.TextField()
    photo = models.ImageField(
        upload_to="team/",
        blank=True,
        null=True,
    )
    qualifications = models.CharField(
        max_length=240,
        blank=True,
        help_text="Only include qualifications that can be supported.",
    )
    languages = models.CharField(
        max_length=200,
        blank=True,
        help_text="For example: English, Luganda and Runyankole.",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(
        default=False,
        help_text="Activate when the profile and photo are approved.",
    )

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} - {self.role}"


class CompanyCredential(models.Model):
    name = models.CharField(
        max_length=150,
        help_text="For example: Uganda Tourism Board operator licence.",
    )
    issuer = models.CharField(
        max_length=150,
        blank=True,
        help_text="Organisation that issued or maintains the credential.",
    )
    identifier = models.CharField(
        max_length=120,
        blank=True,
        help_text="Licence or membership number, if it is public.",
    )
    description = models.CharField(max_length=240, blank=True)
    verification_url = models.URLField(
        help_text="Public page where a traveller can verify this credential.",
    )
    valid_until = models.DateField(
        blank=True,
        null=True,
        help_text="Optional expiry or renewal date shown on the credential.",
    )
    logo = models.ImageField(
        upload_to="credentials/",
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(
        default=False,
        help_text=(
            "Activate only after the name, number and verification link have "
            "been checked."
        ),
    )

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Destination(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(
        upload_to="destinations/",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject or 'No Subject'}"


class GalleryImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"Image {self.id}"
