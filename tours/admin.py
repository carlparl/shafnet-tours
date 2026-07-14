import logging

from django.conf import settings
from django.contrib import admin, messages
from django.core.mail import send_mail

from .models import (
    Booking,
    ContactMessage,
    Destination,
    GalleryImage,
    Itinerary,
    Testimonial,
    Tour,
)


logger = logging.getLogger(__name__)


def send_booking_status_email(booking):
    """Notify a customer after an admin changes the booking status."""
    status_messages = {
        "pending": (
            "Your booking request is being reviewed. We will contact you "
            "after checking availability and final details."
        ),
        "confirmed": (
            "Your booking request has been confirmed. Our team will contact "
            "you with the agreed itinerary and remaining travel details."
        ),
        "cancelled": (
            "Your booking request has been marked as cancelled. Please "
            "contact us if you have questions or would like another option."
        ),
    }
    status_message = status_messages.get(
        booking.status,
        f"Your booking status is now {booking.get_status_display()}.",
    )

    message = (
        f"Hello {booking.full_name},\n\n"
        f"Booking reference: ST-{booking.pk:05d}\n"
        f"Tour: {booking.tour.title}\n"
        f"Status: {booking.get_status_display()}\n\n"
        f"{status_message}\n\n"
        "Shafnet Tours & Travel Ltd\n"
        "+256 778 221 069"
    )

    try:
        send_mail(
            subject=f"Booking ST-{booking.pk:05d}: {booking.get_status_display()}",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            fail_silently=False,
        )
    except Exception:
        logger.exception(
            "Booking %s status changed, but the customer email failed",
            booking.pk,
        )


class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1
    fields = ("day", "title", "description")
    ordering = ("day",)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "target_audience",
        "region",
        "location",
        "duration_days",
        "price",
        "is_featured",
    )
    list_filter = ("target_audience", "region", "is_featured")
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_featured",)
    inlines = [ItineraryInline]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "booking_reference",
        "full_name",
        "tour",
        "preferred_date",
        "number_of_people",
        "status",
        "created_at",
    )
    list_display_links = ("booking_reference", "full_name")
    list_editable = ("status",)
    list_filter = ("status", "created_at", "preferred_date", "tour__target_audience")
    search_fields = ("full_name", "email", "phone", "tour__title")
    readonly_fields = ("booking_reference", "created_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_per_page = 30
    actions = ("mark_confirmed", "mark_pending", "mark_cancelled")
    fieldsets = (
        (
            "Booking",
            {
                "fields": (
                    "booking_reference",
                    "tour",
                    "status",
                    "preferred_date",
                    "number_of_people",
                    "created_at",
                )
            },
        ),
        (
            "Customer",
            {"fields": ("full_name", "email", "phone")},
        ),
        (
            "Additional information",
            {"fields": ("message",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("tour")

    @admin.display(description="Reference", ordering="id")
    def booking_reference(self, obj):
        if not obj.pk:
            return "Assigned after saving"
        return f"ST-{obj.pk:05d}"

    def save_model(self, request, obj, form, change):
        previous_status = None
        if change and obj.pk:
            previous_status = (
                Booking.objects.filter(pk=obj.pk)
                .values_list("status", flat=True)
                .first()
            )

        super().save_model(request, obj, form, change)

        if previous_status and previous_status != obj.status:
            send_booking_status_email(obj)
            self.message_user(
                request,
                f"Booking ST-{obj.pk:05d} updated to {obj.get_status_display()}.",
                messages.SUCCESS,
            )

    def _change_status(self, request, queryset, status):
        changed = 0
        for booking in queryset.exclude(status=status).select_related("tour"):
            booking.status = status
            booking.save(update_fields=["status"])
            send_booking_status_email(booking)
            changed += 1

        self.message_user(
            request,
            f"{changed} booking(s) updated to {dict(Booking.STATUS_CHOICES)[status]}.",
            messages.SUCCESS,
        )

    @admin.action(description="Mark selected bookings as confirmed")
    def mark_confirmed(self, request, queryset):
        self._change_status(request, queryset, "confirmed")

    @admin.action(description="Mark selected bookings as pending")
    def mark_pending(self, request, queryset):
        self._change_status(request, queryset, "pending")

    @admin.action(description="Mark selected bookings as cancelled")
    def mark_cancelled(self, request, queryset):
        self._change_status(request, queryset, "cancelled")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "rating", "is_active", "created_at")
    list_filter = ("rating", "is_active")
    search_fields = ("name", "location", "message")
    list_editable = ("rating", "is_active")


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "order")
    list_editable = ("is_active", "order")
    search_fields = ("name", "description")
    ordering = ("order", "name")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "created_at")
    search_fields = ("full_name", "email", "subject", "message")
    readonly_fields = ("full_name", "email", "subject", "message", "created_at")
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "caption", "created_at")
    search_fields = ("title", "caption")
    ordering = ("-created_at",)


admin.site.site_header = "Shafnet Tours Administration"
admin.site.site_title = "Shafnet Admin"
admin.site.index_title = "Tour and booking management"
