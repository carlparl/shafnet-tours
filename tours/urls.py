from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("domestic-tours/", views.domestic_tours, name="domestic_tours"),
    path("safaris/", views.safaris, name="safaris"),
    path("about/", views.about, name="about"),
    path("gallery/", views.gallery, name="gallery"),
    path("contact/", views.contact, name="contact"),
    path("privacy/", views.privacy_policy, name="privacy_policy"),
    path("terms/", views.terms_and_conditions, name="terms_and_conditions"),
    path("booking-policy/", views.booking_policy, name="booking_policy"),
    path("tours/<slug:slug>/", views.tour_detail, name="tour_detail"),
    path(
        "booking/confirmation/",
        views.booking_confirmation,
        name="booking_confirmation",
    ),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
