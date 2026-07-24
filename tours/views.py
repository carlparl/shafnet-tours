import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BookingForm, ContactForm
from .models import (
    Booking,
    CompanyCredential,
    Destination,
    GalleryImage,
    TeamMember,
    Testimonial,
    Tour,
)


logger = logging.getLogger(__name__)

LEGACY_TOUR_SLUGS = {
    "2-day-bwindi-gorilla-trekking": "3-day-bwindi-gorilla-trekking",
}


def _active_credentials():
    today = timezone.localdate()
    return CompanyCredential.objects.filter(is_active=True).filter(
        Q(valid_until__isnull=True) | Q(valid_until__gte=today)
    )


def _send_booking_emails(booking):
    """Send booking notifications without risking the saved booking."""
    preferred_date = booking.preferred_date or "Not specified"
    message = booking.message or "Not provided"
    advertised_price = booking.tour.price_summary

    admin_message = (
        "A new booking request was submitted.\n\n"
        f"Booking reference: ST-{booking.pk:05d}\n"
        f"Tour: {booking.tour.title}\n"
        f"Customer: {booking.full_name}\n"
        f"Email: {booking.email}\n"
        f"Phone: {booking.phone}\n"
        f"Travellers: {booking.number_of_people}\n"
        f"Preferred date: {preferred_date}\n"
        f"Advertised price: {advertised_price}\n"
        f"Message: {message}\n"
        f"Status: {booking.get_status_display()}"
    )

    customer_message = (
        f"Hello {booking.full_name},\n\n"
        "Thank you for contacting Shafnet Tours & Travel. "
        f"We received your request for {booking.tour.title}.\n\n"
        f"Travellers: {booking.number_of_people}\n"
        f"Preferred date: {preferred_date}\n\n"
        f"Advertised price: {advertised_price}\n\n"
        "Our team will review availability and contact you with the final "
        "itinerary, pricing and next steps. Your request is not confirmed "
        "until you approve the final plan.\n\n"
        "Shafnet Tours & Travel Ltd\n"
        "+256 789 472229"
    )

    try:
        send_mail(
            subject=f"New booking request: {booking.tour.title}",
            message=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.BOOKING_NOTIFICATION_EMAIL],
            fail_silently=False,
        )
        send_mail(
            subject="We received your Shafnet Tours booking request",
            message=customer_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            fail_silently=False,
        )
    except Exception:
        logger.exception(
            "Booking %s was saved, but its email notification failed",
            booking.pk,
        )


def _send_contact_emails(contact_message):
    """Notify Shafnet and acknowledge a saved website enquiry."""
    subject = contact_message.subject or "Website enquiry"
    reference = f"ENQ-{contact_message.pk:05d}"

    admin_message = (
        "A new website enquiry was submitted.\n\n"
        f"Reference: {reference}\n"
        f"Name: {contact_message.full_name}\n"
        f"Email: {contact_message.email}\n"
        f"Subject: {subject}\n\n"
        f"Message:\n{contact_message.message}"
    )
    customer_message = (
        f"Hello {contact_message.full_name},\n\n"
        "Thank you for contacting Shafnet Tours & Travel. "
        f"We received your enquiry ({reference}) and our team will reply "
        "using the contact details you provided.\n\n"
        f"Subject: {subject}\n\n"
        "Shafnet Tours & Travel Ltd\n"
        "+256 789 472229"
    )

    try:
        EmailMessage(
            subject=f"New website enquiry: {subject}",
            body=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.BOOKING_NOTIFICATION_EMAIL],
            reply_to=[contact_message.email],
        ).send(fail_silently=False)
        send_mail(
            subject=f"We received your Shafnet enquiry ({reference})",
            message=customer_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact_message.email],
            fail_silently=False,
        )
    except Exception:
        logger.exception(
            "Contact enquiry %s was saved, but its email notification failed",
            contact_message.pk,
        )
        return False

    return True


def home(request):
    context = {
        "domestic_tours": Tour.objects.filter(
            target_audience="domestic",
            is_featured=True,
            is_active=True,
        )[:3],
        "safari_tours": Tour.objects.filter(
            target_audience="international",
            is_featured=True,
            is_active=True,
        )[:3],
        "destinations": Destination.objects.filter(is_active=True)[:4],
        "testimonials": (
            Testimonial.objects.filter(is_active=True, is_verified=True)
            .exclude(source_name="")
            .exclude(source_url="")[:3]
        ),
        "credentials": _active_credentials()[:4],
    }
    return render(request, "tours/home.html", context)


def _catalogue_context(request, target_audience):
    tours = Tour.objects.filter(
        target_audience=target_audience,
        is_active=True,
    )
    total_tours = tours.count()

    selected_region = request.GET.get("region", "").strip()
    valid_regions = {value for value, _label in Tour.REGION_CHOICES}
    if selected_region in valid_regions:
        tours = tours.filter(region=selected_region)
    else:
        selected_region = ""

    selected_duration = request.GET.get("duration", "").strip()
    duration_filters = {
        "1-3": {"duration_days__lte": 3},
        "4-6": {
            "duration_days__gte": 4,
            "duration_days__lte": 6,
        },
        "7+": {"duration_days__gte": 7},
    }
    if selected_duration in duration_filters:
        tours = tours.filter(**duration_filters[selected_duration])
    else:
        selected_duration = ""

    styles_by_audience = {
        "domestic": {"transfer", "day_trip", "short_escape"},
        "international": {"focused", "combo", "circuit"},
    }
    audience_styles = styles_by_audience.get(target_audience, set())
    style_choices = tuple(
        (value, label)
        for value, label in Tour.JOURNEY_STYLE_CHOICES
        if value in audience_styles
    )
    selected_style = request.GET.get("style", "").strip()
    valid_styles = {value for value, _label in style_choices}
    if selected_style in valid_styles:
        tours = tours.filter(journey_style=selected_style)
    else:
        selected_style = ""

    selected_sort = request.GET.get("sort", "recommended").strip()
    sort_options = {
        "recommended": ("display_order", "title"),
        "shortest": ("duration_days", "display_order", "title"),
        "longest": ("-duration_days", "display_order", "title"),
        "newest": ("-created_at", "title"),
    }
    if selected_sort not in sort_options:
        selected_sort = "recommended"
    tours = tours.order_by(*sort_options[selected_sort])

    return {
        "tours": tours,
        "total_tours": total_tours,
        "selected_region": selected_region,
        "selected_duration": selected_duration,
        "selected_style": selected_style,
        "selected_sort": selected_sort,
        "region_choices": Tour.REGION_CHOICES,
        "style_choices": style_choices,
        "filters_applied": bool(
            selected_region or selected_duration or selected_style
        ),
    }


def domestic_tours(request):
    context = {
        **_catalogue_context(request, "domestic"),
        "page_type": "domestic",
        "page_label": "Explore Uganda locally",
        "page_title": "Domestic tours for refreshing escapes",
        "page_intro": (
            "Discover weekend getaways, group adventures and memorable trips "
            "designed for travellers exploring more of Uganda."
        ),
    }
    return render(request, "tours/tour_list.html", context)


def safaris(request):
    context = {
        **_catalogue_context(request, "international"),
        "page_type": "safari",
        "page_label": "Discover the Pearl of Africa",
        "page_title": "Uganda safaris shaped around you",
        "page_intro": (
            "Explore wildlife, landscapes and local experiences through safari "
            "routes planned with care and local insight."
        ),
    }
    return render(request, "tours/tour_list.html", context)


def about(request):
    return render(
        request,
        "tours/about.html",
        {
            "team_members": TeamMember.objects.filter(is_active=True),
            "credentials": _active_credentials(),
        },
    )


def gallery(request):
    return render(
        request,
        "tours/gallery.html",
        {"images": GalleryImage.objects.all()},
    )


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            email_sent = _send_contact_emails(contact_message)
            if email_sent:
                messages.success(
                    request,
                    "Thank you. Your enquiry has been received and a copy was sent to your email.",
                )
            else:
                messages.warning(
                    request,
                    "Your enquiry was saved, but the confirmation email could not be sent. "
                    "You can also contact us by phone or WhatsApp.",
                )
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "tours/contact.html", {"form": form})


def privacy_policy(request):
    return render(request, "tours/privacy_policy.html")


def terms_and_conditions(request):
    return render(request, "tours/terms_and_conditions.html")


def booking_policy(request):
    return render(request, "tours/booking_policy.html")


def image_credits(request):
    return render(request, "tours/image_credits.html")


def tour_detail(request, slug):
    if slug in LEGACY_TOUR_SLUGS:
        return redirect(
            "tour_detail",
            slug=LEGACY_TOUR_SLUGS[slug],
            permanent=True,
        )

    tour = get_object_or_404(
        Tour.objects.prefetch_related("itineraries"),
        slug=slug,
        is_active=True,
    )

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            accepted_policies = request.POST.get("accept_policies") == "yes"
            if not accepted_policies:
                form.add_error(
                    None,
                    "Please accept the Terms, Booking Policy and Privacy Policy.",
                )
            else:
                booking = form.save(commit=False)
                booking.tour = tour
                booking.save()
                _send_booking_emails(booking)
                request.session["latest_booking_id"] = booking.pk
                return redirect("booking_confirmation")
    else:
        form = BookingForm()

    return render(
        request,
        "tours/tour_detail.html",
        {"tour": tour, "form": form},
    )


def booking_confirmation(request):
    booking_id = request.session.get("latest_booking_id")
    if not booking_id:
        return redirect("home")

    booking = get_object_or_404(
        Booking.objects.select_related("tour"),
        pk=booking_id,
    )
    return render(
        request,
        "tours/booking_confirmation.html",
        {"booking": booking},
    )


def robots_txt(request):
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        f"Sitemap: {sitemap_url}\n"
    )
    return HttpResponse(content, content_type="text/plain")
