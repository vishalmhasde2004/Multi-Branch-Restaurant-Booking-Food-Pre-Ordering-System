from django.contrib import admin

from .models import Booking, Table


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'location',
        'table',
        'date',
        'time',
        'guests',
        'status',
        'created_at',
    )

    list_filter = (
        'location',
        'date',
        'status',
    )

    search_fields = (
        'user__username',
        'location',
    )

    list_editable = (
        'status',
    )

    ordering = (
        '-date',
        '-time',
    )

    readonly_fields = (
        'created_at',
    )

    fieldsets = (
        (
            'Booking Information',
            {
                'fields': (
                    'user',
                    'location',
                    'table',
                    'date',
                    'time',
                    'guests',
                    'status',
                    'created_at',
                )
            }
        ),
    )


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'location',
        'table_number',
        'capacity',
        'is_available',
    )

    list_filter = (
        'location',
        'is_available',
    )

    search_fields = (
        'location',
    )

    list_editable = (
        'is_available',
    )

    ordering = (
        'location',
        'table_number',
    )