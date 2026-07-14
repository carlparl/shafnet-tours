from django.contrib import admin

from .models import (
    Booking,
    ContactMessage,
    Destination,
    GalleryImage,
    Itinerary,
    Testimonial,
    Tour,
)


class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "target_audience",
        "region",
        "location",
        "duration_days",
        "is_featured",
    )
    list_filter = ("target_audience", "region", "is_featured")
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("target_audience", "is_featured")
    inlines = [ItineraryInline]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "tour",
        "email",
        "number_of_people",
        "preferred_date",
        "status",
        "created_at",
    )
    list_filter = ("status", "tour__target_audience")
    search_fields = ("full_name", "email", "tour__title")
    list_editable = ("status",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
        "rating",
        "is_active",
        "created_at",
    )
    list_filter = ("rating", "is_active")
    search_fields = ("name", "location", "message")
    list_editable = ("rating", "is_active")


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "order")
    list_editable = ("is_active", "order")
    search_fields = ("name", "description")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "created_at")
    search_fields = ("full_name", "email", "subject", "message")
    readonly_fields = ("created_at",)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "caption", "created_at")
    search_fields = ("title", "caption")