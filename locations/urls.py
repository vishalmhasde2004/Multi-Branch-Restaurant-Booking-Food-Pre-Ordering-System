from django.urls import path
from .views import locations, surat, delhi, pune

urlpatterns = [
    path('', locations, name='locations'),
    path('surat/', surat, name='surat'),
    path('delhi/', delhi, name='delhi'),
    path('pune/', pune, name='pune'),
]