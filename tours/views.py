import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm, ContactForm
from .models import Destination, GalleryImage, Testimonial, Tour


logger = logging.getLogger(__name__)


def _send_admin_email(subject, message):
    """Notify the team without making a successful form submission fail."""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.BOOKING_NOTIFICATION_EMAIL],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Could not send Shafnet Tours enquiry notification")


def home(request):
    domestic_tours = Tour.objects.filter(target_audience='domestic', is_featured=True)[:3]
    international_tours = Tour.objects.filter(target_audience='international', is_featured=True)[:3]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    destinations = Destination.objects.filter(is_active=True)[:8]

    context = {
        'domestic_tours': domestic_tours,
        'international_tours': international_tours,
        'testimonials': testimonials,
        'destinations': destinations,
    }
    return render(request, 'tours/home.html', context)


def tour_list(request):
    tours = Tour.objects.all()

    audience = request.GET.get('audience')
    region = request.GET.get('region')
    valid_audiences = {value for value, _ in Tour.AUDIENCE_CHOICES}
    valid_regions = {value for value, _ in Tour.REGION_CHOICES}

    if audience not in valid_audiences:
        audience = None
    if region not in valid_regions or audience != 'international':
        region = None

    if audience:
        tours = tours.filter(target_audience=audience)

    if region:
        tours = tours.filter(region=region)

    context = {
        'tours': tours,
        'current_audience': audience,
        'current_region': region,
    }
    return render(request, 'tours/tour_list.html', context)


def tour_detail(request, slug):
    tour = get_object_or_404(Tour.objects.prefetch_related('itineraries'), slug=slug)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour
            booking.save()

            subject = f"New Booking Request: {tour.title}"
            email_message = (
                "New booking request received.\n\n"
                f"Tour: {tour.title}\n"
                f"Name: {booking.full_name}\n"
                f"Email: {booking.email}\n"
                f"Phone: {booking.phone}\n"
                f"Number of people: {booking.number_of_people}\n"
                f"Preferred date: {booking.preferred_date or 'Not provided'}\n"
                f"Message: {booking.message or 'Not provided'}"
            )
            _send_admin_email(subject, email_message)

            messages.success(request, "Thank you! Your booking request has been received. We'll contact you shortly.")
            return redirect('tour_detail', slug=tour.slug)
    else:
        form = BookingForm()

    context = {
        'tour': tour,
        'form': form,
    }
    return render(request, 'tours/tour_detail.html', context)


def about(request):
    return render(request, 'tours/about.html')


def gallery(request):
    images = GalleryImage.objects.all()
    context = {'images': images}
    return render(request, 'tours/gallery.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            subject = contact_message.subject or 'Website enquiry'
            email_message = (
                "New website enquiry received.\n\n"
                f"Name: {contact_message.full_name}\n"
                f"Email: {contact_message.email}\n"
                f"Subject: {subject}\n"
                f"Message: {contact_message.message}"
            )
            _send_admin_email(f"New Website Enquiry: {subject}", email_message)
            messages.success(request, "Thank you! Your message has been sent. We'll get back to you soon.")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'tours/contact.html', {'form': form})
