from django.urls import path
from .views import booking_home, my_bookings, cancel_booking

urlpatterns = [
    path('', booking_home, name='booking'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
]