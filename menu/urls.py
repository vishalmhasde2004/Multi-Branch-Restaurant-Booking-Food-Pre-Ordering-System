from django.urls import path

from .views import menu_home


urlpatterns = [
    path('', menu_home, name='menu'),
]