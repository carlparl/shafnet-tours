import logging

from django.conf import settings
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.html import format_html

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
    """Notify a customer after an administrator changes the booking status."""
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
        return False

    return True


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
        "currency",
        "price_basis",
        "price_is_from",
        "is_featured",
    )
    list_filter = (
        "target_audience",
        "currency",
        "price_basis",
        "price_is_from",
        "region",
        "is_featured",
    )
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_featured",)
    list_per_page = 30
    inlines = [ItineraryInline]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "booking_reference",
        "full_name",
        "customer_email",
        "customer_phone",
        "tour",
        "preferred_date",
        "travel_timing",
        "number_of_people",
        "status_badge",
        "created_at",
    )
    list_display_links = ("booking_reference", "full_name")
    list_filter = (
        "status",
        ("created_at", admin.DateFieldListFilter),
        ("preferred_date", admin.DateFieldListFilter),
        "tour__target_audience",
        "tour",
    )
    search_fields = (
        "=id",
        "full_name",
        "email",
        "phone",
        "tour__title",
    )
    search_help_text = (
        "Search by booking number, customer name, email, phone, or tour."
    )
    readonly_fields = (
        "booking_reference",
        "travel_timing",
        "created_at",
    )
    autocomplete_fields = ("tour",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_select_related = ("tour",)
    list_per_page = 30
    save_on_top = True
    actions = ("mark_confirmed", "mark_pending", "mark_cancelled")
    actions_on_top = True
    actions_on_bottom = True
    empty_value_display = "—"
    fieldsets = (
        (
            "Booking",
            {
                "fields": (
                    "booking_reference",
                    "tour",
                    "status",
                    "preferred_date",
                    "travel_timing",
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

    @admin.display(description="Reference", ordering="id")
    def booking_reference(self, obj):
        if not obj or not obj.pk:
            return "Assigned after saving"
        return f"ST-{obj.pk:05d}"

    @admin.display(description="Email", ordering="email")
    def customer_email(self, obj):
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)

    @admin.display(description="Phone", ordering="phone")
    def customer_phone(self, obj):
        phone_uri = "".join(
            character
            for character in obj.phone
            if character.isdigit() or character == "+"
        )
        return format_html('<a href="tel:{}">{}</a>', phone_uri, obj.phone)

    @admin.display(description="Travel", ordering="preferred_date")
    def travel_timing(self, obj):
        if not obj or not obj.preferred_date:
            return format_html('<span style="color:#6b7280;">Not selected</span>')

        days = (obj.preferred_date - timezone.localdate()).days
        if days < 0:
            label = "Past"
            color = "#6b7280"
        elif days == 0:
            label = "Today"
            color = "#dc2626"
        elif days == 1:
            label = "Tomorrow"
            color = "#d97706"
        else:
            label = f"In {days} days"
            color = "#047857"

        return format_html(
            '<strong style="color:{};">{}</strong>',
            color,
            label,
        )

    @admin.display(description="Status", ordering="status")
    def status_badge(self, obj):
        styles = {
            "pending": ("#92400e", "#fef3c7"),
            "confirmed": ("#166534", "#dcfce7"),
            "cancelled": ("#991b1b", "#fee2e2"),
        }
        foreground, background = styles.get(
            obj.status,
            ("#374151", "#f3f4f6"),
        )
        return format_html(
            '<span style="display:inline-block;padding:4px 9px;border-radius:999px;'
            'font-weight:700;color:{};background:{};">{}</span>',
            foreground,
            background,
            obj.get_status_display(),
        )

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
            email_sent = send_booking_status_email(obj)
            if email_sent:
                self.message_user(
                    request,
                    (
                        f"Booking ST-{obj.pk:05d} updated to "
                        f"{obj.get_status_display()}, and the customer was notified."
                    ),
                    messages.SUCCESS,
                )
            else:
                self.message_user(
                    request,
                    (
                        f"Booking ST-{obj.pk:05d} was updated, but the customer "
                        "email failed. Check the server and Brevo logs."
                    ),
                    messages.WARNING,
                )

    def _change_status(self, request, queryset, status):
        changed = 0
        emails_sent = 0
        emails_failed = 0

        for booking in queryset.exclude(status=status).select_related("tour"):
            booking.status = status
            booking.save(update_fields=["status"])
            if send_booking_status_email(booking):
                emails_sent += 1
            else:
                emails_failed += 1
            changed += 1

        status_label = dict(Booking.STATUS_CHOICES)[status]
        if changed == 0:
            self.message_user(
                request,
                f"No bookings required a change to {status_label}.",
                messages.INFO,
            )
            return

        summary = (
            f"{changed} booking(s) updated to {status_label}. "
            f"{emails_sent} customer email(s) sent."
        )
        if emails_failed:
            summary += (
                f" {emails_failed} email(s) failed; check the server and Brevo logs."
            )

        self.message_user(
            request,
            summary,
            messages.WARNING if emails_failed else messages.SUCCESS,
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
    list_filter = (("created_at", admin.DateFieldListFilter),)
    search_fields = ("full_name", "email", "subject", "message")
    readonly_fields = ("full_name", "email", "subject", "message", "created_at")
    date_hierarchy = "created_at"
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
