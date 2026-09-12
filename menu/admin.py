from django.contrib import admin

from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'category',
        'location',
        'price',
        'is_available',
        'created_at',
    )

    list_filter = (
        'category',
        'location',
        'is_available',
    )

    search_fields = (
        'name',
        'description',
    )

    list_editable = (
        'price',
        'is_available',
    )

    ordering = (
        'location',
        'category',
        'name',
    )

    readonly_fields = (
        'created_at',
    )

    fieldsets = (
        (
            'Menu Information',
            {
                'fields': (
                    'name',
                    'description',
                    'category',
                    'location',
                    'image',
                )
            }
        ),

        (
            'Pricing & Availability',
            {
                'fields': (
                    'price',
                    'is_available',
                    'created_at',
                )
            }
        ),
    )