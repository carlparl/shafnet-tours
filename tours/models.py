from django.db import models
from django.utils.text import slugify

class Tour(models.Model):
    AUDIENCE_CHOICES = [
        ('domestic', 'Domestic Tours'),
        ('international', 'International Safaris'),
    ]

    REGION_CHOICES = [
        ('central', 'Central Uganda'),
        ('western', 'Western Uganda'),
        ('northern', 'Northern Uganda'),
        ('eastern', 'Eastern Uganda'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duration_days = models.PositiveIntegerField()
    location = models.CharField(max_length=200)
    target_audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default='international')
    region = models.CharField(max_length=20, choices=REGION_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to='tours/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Itinerary(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='itineraries')
    day = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        ordering = ['day']

    def __str__(self):
        return f"Day {self.day} - {self.title}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    number_of_people = models.PositiveIntegerField(default=1)
    preferred_date = models.DateField(null=True, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.tour.title}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    rating = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.rating} stars"


class Destination(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject or 'No Subject'}"


class GalleryImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"Image {self.id}"