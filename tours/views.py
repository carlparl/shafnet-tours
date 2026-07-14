from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from tours.forms import ContactForm
from .models import GalleryImage, Testimonial, Tour, Destination
from .forms import BookingForm
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    featured_tours = Tour.objects.filter(is_featured=True)[:6]
    domestic_tours = Tour.objects.filter(target_audience='domestic', is_featured=True)[:3]
    international_tours = Tour.objects.filter(target_audience='international', is_featured=True)[:3]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    
    # Add this line
    destinations = Destination.objects.filter(is_active=True)[:8]

    context = {
        'featured_tours': featured_tours,
        'domestic_tours': domestic_tours,
        'international_tours': international_tours,
        'testimonials': testimonials,
        'destinations': destinations,          # ← Add this
    }
    return render(request, 'tours/home.html', context)
def tour_list(request):
    tours = Tour.objects.all()

    # Get filter values from URL
    audience = request.GET.get('audience')      # 'domestic' or 'international'
    region = request.GET.get('region')          # 'western', 'northern', etc.

    if audience == 'domestic':
        tours = tours.filter(target_audience='domestic')
    elif audience == 'international':
        tours = tours.filter(target_audience='international')

    if region:
        tours = tours.filter(region=region)

    context = {
        'tours': tours,
        'current_audience': audience,
        'current_region': region,
    }
    return render(request, 'tours/tour_list.html', context)

def tour_detail(request, slug):
    tour = get_object_or_404(Tour, slug=slug)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour
            booking.save()

            # Send email notification
            subject = f"New Booking Request: {tour.title}"
            message = f"""
New booking received!

Tour: {tour.title}
Name: {booking.full_name}
Email: {booking.email}
Phone: {booking.phone}
Number of People: {booking.number_of_people}
Preferred Date: {booking.preferred_date}
Message: {booking.message}
"""

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['info@shafnettours.com'],
                fail_silently=False,
            )

            messages.success(request, "Thank you! Your booking request has been received. We'll contact you shortly.")
            return redirect('tour_detail', slug=tour.slug)
        else:
            # Form is invalid - show errors
            pass
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
            form.save()
            messages.success(request, "Thank you! Your message has been sent. We'll get back to you soon.")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'tours/contact.html', {'form': form})