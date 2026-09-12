from django.db import models
from django.contrib.auth.models import User


class Table(models.Model):

    location = models.CharField(max_length=100)

    table_number = models.IntegerField()

    capacity = models.IntegerField()

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.location.title()} - Table {self.table_number}"


class Booking(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    location = models.CharField(max_length=100)

    table = models.ForeignKey(
        Table,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    date = models.DateField()

    time = models.TimeField()

    guests = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.location}"