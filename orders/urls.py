from django.urls import path

from .views import (
    my_orders,
    add_to_cart,
    cart,
    increase_quantity,
    decrease_quantity,
    remove_from_cart,
    checkout,
    delivery_checkout,
    cancel_order,
)


urlpatterns = [


    path('my-orders/', my_orders, name='my_orders'),

    path(
        'add/<int:menu_item_id>/',
        add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/',
        cart,
        name='cart'
    ),

    path(
        'increase/<int:cart_item_id>/',
        increase_quantity,
        name='increase_quantity'
    ),

    path(
        'decrease/<int:cart_item_id>/',
        decrease_quantity,
        name='decrease_quantity'
    ),

    path(
    'remove/<int:cart_item_id>/',
    remove_from_cart,
    name='remove_from_cart'
),

    path(
    'checkout/',
    checkout,
    name='checkout'
),

path(
    'delivery-checkout/',
    delivery_checkout,
    name='delivery_checkout'
),

path(
    'cancel/<int:order_id>/',
    cancel_order,
    name='cancel_order'
),
]