from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem
from booking.models import Booking


class Order(models.Model):

    ORDER_TYPE_CHOICES = [
        ('DINE_IN', 'Dine-in / Table Pre-Order'),
        ('DELIVERY', 'Online Delivery'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('ONLINE', 'Pay Online'),
        ('COD', 'Pay After Delivery'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('NOT_REQUIRED', 'Not Required'),
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
    ]

    DELIVERY_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Preparing', 'Preparing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    DINE_IN_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Preparing', 'Preparing'),
        ('Ready', 'Ready'),
        ('Served', 'Served'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    order_type = models.CharField(
        max_length=20,
        choices=ORDER_TYPE_CHOICES
    )

    location = models.CharField(
        max_length=20
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        null=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='NOT_REQUIRED'
    )

    full_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    delivery_address = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.SET_NULL,
        null=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.menu_item} x {self.quantity}"


class CartItem(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    added_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.menu_item.name}"