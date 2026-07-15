import logging

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm
from .models import Booking, Destination, Testimonial, Tour


logger = logging.getLogger(__name__)


def _send_booking_emails(booking):
    """Send booking notifications without risking the saved booking."""
    preferred_date = booking.preferred_date or "Not specified"
    message = booking.message or "Not provided"

    admin_message = (
        "A new booking request was submitted.\n\n"
        f"Booking reference: ST-{booking.pk:05d}\n"
        f"Tour: {booking.tour.title}\n"
        f"Customer: {booking.full_name}\n"
        f"Email: {booking.email}\n"
        f"Phone: {booking.phone}\n"
        f"Travellers: {booking.number_of_people}\n"
        f"Preferred date: {preferred_date}\n"
        f"Message: {message}\n"
        f"Status: {booking.get_status_display()}"
    )

    customer_message = (
        f"Hello {booking.full_name},\n\n"
        "Thank you for contacting Shafnet Tours & Travel. "
        f"We received your request for {booking.tour.title}.\n\n"
        f"Travellers: {booking.number_of_people}\n"
        f"Preferred date: {preferred_date}\n\n"
        "Our team will review availability and contact you with the final "
        "itinerary, pricing and next steps. Your request is not confirmed "
        "until you approve the final plan.\n\n"
        "Shafnet Tours & Travel Ltd\n"
        "+256 778 221 069"
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


def home(request):
    context = {
        "domestic_tours": Tour.objects.filter(
            target_audience="domestic",
            is_featured=True,
        )[:3],
        "safari_tours": Tour.objects.filter(
            target_audience="international",
            is_featured=True,
        )[:3],
        "destinations": Destination.objects.filter(is_active=True)[:4],
        "testimonials": Testimonial.objects.filter(is_active=True)[:3],
    }
    return render(request, "tours/home.html", context)


def domestic_tours(request):
    context = {
        "tours": Tour.objects.filter(target_audience="domestic"),
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
        "tours": Tour.objects.filter(target_audience="international"),
        "page_type": "safari",
        "page_label": "Discover the Pearl of Africa",
        "page_title": "Uganda safaris shaped around you",
        "page_intro": (
            "Explore wildlife, landscapes and local experiences through safari "
            "routes planned with care and local insight."
        ),
    }
    return render(request, "tours/tour_list.html", context)


def privacy_policy(request):
    return render(request, "tours/privacy_policy.html")


def terms_and_conditions(request):
    return render(request, "tours/terms_and_conditions.html")


def booking_policy(request):
    return render(request, "tours/booking_policy.html")


def tour_detail(request, slug):
    tour = get_object_or_404(
        Tour.objects.prefetch_related("itineraries"),
        slug=slug,
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
