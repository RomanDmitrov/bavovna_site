from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_create, name='booking_create'),
    path('success/', views.booking_success, name='booking_success'),
    path('partnership/', views.partnership, name='partnership'),
]