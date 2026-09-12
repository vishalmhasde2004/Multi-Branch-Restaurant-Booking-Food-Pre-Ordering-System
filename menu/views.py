from django.shortcuts import render

from .models import MenuItem


def menu_home(request):

    selected_category = request.GET.get(
        'category',
        ''
    )

    selected_location = request.GET.get(
        'location',
        ''
    )

    menu_items = MenuItem.objects.filter(
        is_available=True
    )

    if selected_location:

        menu_items = menu_items.filter(
            location=selected_location
        )

    if selected_category:

        menu_items = menu_items.filter(
            category=selected_category
        )

    menu_items = menu_items.order_by(
        'category',
        'name'
    )

    categories = [
        'Starter',
        'Main Course',
        'Dessert',
        'Drinks',
    ]

    locations = [
        ('surat', 'Surat'),
        ('delhi', 'Delhi'),
        ('pune', 'Pune'),
    ]

    return render(
        request,
        'menu/menu.html',
        {
            'menu_items': menu_items,
            'categories': categories,
            'locations': locations,
            'selected_category': selected_category,
            'selected_location': selected_location,
        }
    )