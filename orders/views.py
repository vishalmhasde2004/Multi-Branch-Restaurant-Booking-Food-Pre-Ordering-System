from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from menu.models import MenuItem
from .models import CartItem, Order, OrderItem


@login_required
def my_orders(request):

    orders = (
        Order.objects
        .filter(user=request.user)
        .select_related('booking')
        .prefetch_related('items__menu_item')
        .order_by('-created_at')
    )

    # Create tracking steps for every order
    for order in orders:

        # -----------------------------------------
        # DELIVERY ORDER TRACKING
        # -----------------------------------------

        if order.order_type == 'DELIVERY':

            tracking_names = [
                'Pending',
                'Confirmed',
                'Preparing',
                'Out for Delivery',
                'Delivered',
            ]

        # -----------------------------------------
        # DINE-IN ORDER TRACKING
        # -----------------------------------------

        else:

            tracking_names = [
                'Pending',
                'Confirmed',
                'Preparing',
                'Ready',
                'Served',
                'Completed',
            ]

        tracking_steps = []

        # -----------------------------------------
        # CANCELLED ORDER
        # -----------------------------------------

        if order.status == 'Cancelled':

            tracking_steps.append({
                'name': 'Cancelled',
                'state': 'cancelled',
            })

        # -----------------------------------------
        # NORMAL ORDER
        # -----------------------------------------

        else:

            try:
                current_index = tracking_names.index(order.status)
            except ValueError:
                current_index = 0

            for index, step_name in enumerate(tracking_names):

                if index < current_index:

                    state = 'completed'

                elif index == current_index:

                    state = 'current'

                else:

                    state = 'upcoming'

                tracking_steps.append({
                    'name': step_name,
                    'state': state,
                })

        order.tracking_steps = tracking_steps

    return render(
        request,
        'orders/my_orders.html',
        {
            'orders': orders,
        }
    )


# =========================================
# ADD TO CART
# =========================================

@login_required
def add_to_cart(request, menu_item_id):

    menu_item = get_object_or_404(
        MenuItem,
        id=menu_item_id,
        is_available=True
    )

    # Check user's existing cart
    existing_cart = CartItem.objects.filter(
        user=request.user
    ).select_related('menu_item')

    # If cart already has another location
    if existing_cart.exists():

        cart_location = existing_cart.first().menu_item.location

        if cart_location != menu_item.location:

            return render(
                request,
                'orders/cart_location_error.html',
                {
                    'current_location': cart_location,
                    'new_location': menu_item.location,
                }
            )

    # Add item to cart
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        menu_item=menu_item
    )

    if not created:

        cart_item.quantity += 1
        cart_item.save()

    return redirect('menu')

# =========================================
# CART
# =========================================

@login_required
def cart(request):

    cart_items = (
        CartItem.objects
        .filter(user=request.user)
        .select_related('menu_item')
    )

    total = sum(
        item.menu_item.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        'orders/cart.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


# =========================================
# INCREASE QUANTITY
# =========================================

@login_required
def increase_quantity(request, cart_item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        user=request.user
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')


# =========================================
# DECREASE QUANTITY
# =========================================

@login_required
def decrease_quantity(request, cart_item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        user=request.user
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart')


# =========================================
# REMOVE FROM CART
# =========================================

@login_required
def remove_from_cart(request, cart_item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        user=request.user
    )

    cart_item.delete()

    return redirect('cart')


# =========================================
# CHECKOUT
# =========================================

@login_required
def checkout(request):

    cart_items = (
        CartItem.objects
        .filter(user=request.user)
        .select_related('menu_item')
    )

    if not cart_items.exists():

        return redirect('cart')

    total = sum(
        item.menu_item.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        'orders/checkout.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


# =========================================
# DELIVERY CHECKOUT
# =========================================

@login_required
def delivery_checkout(request):

    cart_items = (
        CartItem.objects
        .filter(user=request.user)
        .select_related('menu_item')
    )

    if not cart_items.exists():

        return redirect('cart')

    total = sum(
        item.menu_item.price * item.quantity
        for item in cart_items
    )

    if request.method == 'POST':

        full_name = request.POST.get(
            'full_name',
            ''
        )

        phone = request.POST.get(
            'phone',
            ''
        )

        address = request.POST.get(
            'address',
            ''
        )

        payment_method = request.POST.get(
            'payment_method',
            ''
        )

        # -----------------------------------------
        # PAYMENT METHOD
        # -----------------------------------------

        if payment_method == 'online':

            order_payment_method = 'ONLINE'
            payment_status = 'PENDING'

        elif payment_method == 'cod':

            order_payment_method = 'COD'
            payment_status = 'PENDING'

        else:

            return render(
                request,
                'orders/delivery_checkout.html',
                {
                    'cart_items': cart_items,
                    'total': total,
                    'error': 'Please select a payment method.',
                }
            )

        # -----------------------------------------
        # CREATE DELIVERY ORDER
        # -----------------------------------------

        order = Order.objects.create(

            user=request.user,

            order_type='DELIVERY',

            location=cart_items.first().menu_item.location,

            total_amount=total,

            payment_method=order_payment_method,

            payment_status=payment_status,

            full_name=full_name,

            phone=phone,

            delivery_address=address,

            status='Pending'
        )

        # -----------------------------------------
        # CREATE ORDER ITEMS
        # -----------------------------------------

        for cart_item in cart_items:

            OrderItem.objects.create(

                order=order,

                menu_item=cart_item.menu_item,

                quantity=cart_item.quantity,

                price=cart_item.menu_item.price
            )

        # -----------------------------------------
        # CLEAR CART
        # -----------------------------------------

        cart_items.delete()

        return render(
            request,
            'orders/delivery_checkout.html',
            {
                'order': order,
                'success': (
                    'Your delivery order has '
                    'been placed successfully!'
                ),
            }
        )

    return render(
        request,
        'orders/delivery_checkout.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    # Orders that cannot be cancelled
    non_cancellable_statuses = [
        'Out for Delivery',
        'Delivered',
        'Served',
        'Completed',
        'Cancelled',
    ]

    if order.status not in non_cancellable_statuses:

        order.status = 'Cancelled'
        order.save()

    return redirect('my_orders')