from django.db import models


class MenuItem(models.Model):

    CATEGORY_CHOICES = [
        ('Starter', 'Starter'),
        ('Main Course', 'Main Course'),
        ('Dessert', 'Dessert'),
        ('Drinks', 'Drinks'),
    ]

    LOCATION_CHOICES = [
        ('surat', 'Surat'),
        ('delhi', 'Delhi'),
        ('pune', 'Pune'),
    ]

    name = models.CharField(max_length=150)

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    location = models.CharField(
        max_length=20,
        choices=LOCATION_CHOICES
    )

    image = models.ImageField(
        upload_to='menu/',
        blank=True,
        null=True
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.location.title()}"