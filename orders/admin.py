from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Order, OrderItem, CartItem


class OrderItemInline(admin.TabularInline):
    """Allows viewing and editing ordered food items directly inside the Order page."""
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)
    fields = ('menu_item', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    # Display Order Items inline on the details page
    inlines = [OrderItemInline]

    list_display = (
        'id',
        'customer_name',
        'get_order_type_badge',
        'location',
        'total_amount',
        'payment_method',
        'payment_status',
        'status',
        'created_at',
    )

    list_filter = (
        'order_type',
        'status',
        'payment_status',
        'location',
        ('created_at', admin.DateFieldListFilter),
    )

    search_fields = (
        'id',
        'user__username',
        'full_name',
        'phone',
        'delivery_address',
    )

    list_editable = (
        'payment_status',
        'status',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
    )

    date_hierarchy = 'created_at'

    fieldsets = (
        (
            'Order Overview',
            {
                'fields': (
                    'user',
                    'order_type',
                    'booking',
                    'location',
                    'status',
                    'created_at',
                )
            }
        ),
        (
            'Payment Details',
            {
                'fields': (
                    'total_amount',
                    'payment_method',
                    'payment_status',
                )
            }
        ),
        (
            'Customer & Delivery Information',
            {
                'fields': (
                    'full_name',
                    'phone',
                    'delivery_address',
                )
            }
        ),
    )

    @admin.display(description='Customer')
    def customer_name(self, obj):
        return obj.full_name or obj.user.username

    @admin.display(description='Order Type')
    def get_order_type_badge(self, obj):
        if obj.order_type == 'DINE_IN':
            return mark_safe(
                '<span style="background-color: #28a745; color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 11px; display: inline-block; white-space: nowrap; line-height: 1.2;">🍽️ Dine-in</span>'
            )
        elif obj.order_type == 'DELIVERY':
            return mark_safe(
                '<span style="background-color: #007bff; color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 11px; display: inline-block; white-space: nowrap; line-height: 1.2;">🛵 Delivery</span>'
            )
        return obj.get_order_type_display()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'order',
        'menu_item',
        'quantity',
        'price',
    )

    search_fields = (
        'order__id',
        'order__user__username',
        'menu_item__name',
    )

    list_filter = (
        'menu_item',
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'menu_item',
        'quantity',
        'added_at',
    )

    search_fields = (
        'user__username',
        'menu_item__name',
    )

    list_filter = (
        'added_at',
    )

    list_editable = (
        'quantity',
    )
    
    ordering = (
        '-added_at',
    )