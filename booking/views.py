from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Booking, Table
from orders.models import CartItem, Order, OrderItem


@login_required
def booking_home(request):

    available_tables = []

    location = ''
    date = ''
    time = ''
    guests = ''
    table_id = ''

    no_table_message = ''
    error_message = ''

    booking = None
    dine_in_order = None

    cart_items = CartItem.objects.filter(
        user=request.user
    ).select_related('menu_item')

    food_total = sum(
        item.menu_item.price * item.quantity
        for item in cart_items
    )


    if request.method == 'POST':

        location = request.POST.get(
            'location',
            ''
        )

        date = request.POST.get(
            'date',
            ''
        )

        time = request.POST.get(
            'time',
            ''
        )

        guests = request.POST.get(
            'guests',
            ''
        )

        table_id = request.POST.get(
            'table',
            ''
        )


        # Validate guests

        if guests:

            try:

                guests = int(guests)

            except ValueError:

                error_message = (
                    'Please enter a valid number of guests.'
                )

        else:

            error_message = (
                'Please select number of guests.'
            )


        # Validate date

        selected_date = None

        if date:

            try:

                selected_date = datetime.strptime(
                    date,
                    '%Y-%m-%d'
                ).date()

            except ValueError:

                error_message = (
                    'Please select a valid date.'
                )

        else:

            error_message = (
                'Please select a booking date.'
            )


        # Date cannot be in the past

        if selected_date:

            today = timezone.localdate()

            if selected_date < today:

                error_message = (
                    'Please select today or a future date.'
                )


        # Validate time

        selected_time = None

        if time:

            try:

                selected_time = datetime.strptime(
                    time,
                    '%H:%M'
                ).time()

            except ValueError:

                error_message = (
                    'Please select a valid time.'
                )

        else:

            error_message = (
                'Please select a booking time.'
            )


        # If booking is today,
        # time must be in the future

        if (
            selected_date
            and selected_time
            and selected_date == timezone.localdate()
        ):

            current_time = timezone.localtime().time()

            if selected_time <= current_time:

                error_message = (
                    'Please select a future time.'
                )


        # Find available tables

        if not error_message:

            available_tables = Table.objects.filter(
                location=location,
                capacity__gte=guests,
                is_available=True
            )


            booked_table_ids = Booking.objects.filter(
                location=location,
                date=date,
                time=time,
                status__in=[
                    'Pending',
                    'Confirmed'
                ]
            ).values_list(
                'table_id',
                flat=True
            )


            available_tables = available_tables.exclude(
                id__in=booked_table_ids
            )


            # No table available

            if not available_tables and not table_id:

                no_table_message = (
                    'Sorry, no table is available '
                    'for this date and time.'
                )


            # Customer selected a table

            if table_id:

                selected_table = available_tables.filter(
                    id=table_id
                ).first()


                if selected_table:

                    # Create table booking

                    booking = Booking.objects.create(
                        user=request.user,
                        location=location,
                        table=selected_table,
                        date=date,
                        time=time,
                        guests=guests
                    )


                    # Create Dine-in Order only if
                    # customer selected food

                    if cart_items.exists():

                        dine_in_order = Order.objects.create(
                            user=request.user,
                            booking=booking,
                            order_type='DINE_IN',
                            location=location,
                            total_amount=food_total,
                            payment_method=None,
                            payment_status='NOT_REQUIRED',
                            full_name=(
                                request.user.get_full_name()
                                or request.user.username
                            ),
                            phone='',
                            delivery_address=None,
                            status='Pending'
                        )


                        # Create Order Items

                        for cart_item in cart_items:

                            OrderItem.objects.create(
                                order=dine_in_order,
                                menu_item=cart_item.menu_item,
                                quantity=cart_item.quantity,
                                price=cart_item.menu_item.price
                            )


                        # Clear cart after saving
                        # the dine-in food pre-order

                        cart_items.delete()


                    # Confirmation page

                    return render(
                        request,
                        'booking/booking.html',
                        {
                            'success': (
                                'Table booking and food '
                                'pre-order submitted successfully!'
                            ),

                            'booking': booking,

                            'dine_in_order': dine_in_order,

                            'cart_items': [],

                            'food_total': food_total,
                        }
                    )


                else:

                    error_message = (
                        'This table is no longer available. '
                        'Please select another table.'
                    )


    return render(
        request,
        'booking/booking.html',
        {
            'available_tables': available_tables,

            'selected_location': location,

            'selected_date': date,

            'selected_time': time,

            'selected_guests': guests,

            'no_table_message': no_table_message,

            'error_message': error_message,

            'today': timezone.localdate(),

            'cart_items': cart_items,

            'food_total': food_total,

            'booking': booking,

            'dine_in_order': dine_in_order,
        }
    )


@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )


    return render(
        request,
        'booking/my_bookings.html',
        {
            'bookings': bookings
        }
    )


@login_required
def cancel_booking(request, booking_id):

    booking = Booking.objects.filter(
        id=booking_id,
        user=request.user
    ).first()


    if booking:

        if booking.status == 'Pending':

            booking.status = 'Cancelled'

            booking.save()


    return redirect('my_bookings')