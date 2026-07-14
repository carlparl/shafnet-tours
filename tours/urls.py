from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("domestic-tours/", views.domestic_tours, name="domestic_tours"),
    path("safaris/", views.safaris, name="safaris"),
    path("tours/<slug:slug>/", views.tour_detail, name="tour_detail"),
    path(
        "booking/confirmation/",
        views.booking_confirmation,
        name="booking_confirmation",
    ),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
