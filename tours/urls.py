from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tours/', views.tour_list, name='tour_list'),
    path('tours/<slug:slug>/', views.tour_detail, name='tour_detail'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
]