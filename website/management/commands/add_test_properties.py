"""
Management command to add test properties for development.
Usage: python manage.py add_test_properties
"""
from django.core.management.base import BaseCommand
from wagtail.models import Page
from website.models import PropertyIndexPage, PropertyPage


class Command(BaseCommand):
    help = 'Add test properties to the database'

    def handle(self, *args, **options):
        # Get or find the PropertyIndexPage
        try:
            index_page = PropertyIndexPage.objects.first()
            if not index_page:
                self.stdout.write(self.style.ERROR('PropertyIndexPage not found. Please create it first in Wagtail admin.'))
                return
        except PropertyIndexPage.DoesNotExist:
            self.stdout.write(self.style.ERROR('PropertyIndexPage not found. Please create it first in Wagtail admin.'))
            return

        # Test properties data
        properties_data = [
            {
                'title': 'Modern City Apartment - Leith',
                'address': '42 Shore Lane, Leith, Edinburgh EH6 4LP',
                'price': 325000,
                'bedrooms': 2,
                'bathrooms': 1,
                'sqft': 850,
                'property_type': 'flat',
                'year': 2015,
                'parking_spaces': 1,
                'reception_rooms': 1,
                'energy_rating': 'C',
                'has_garden': False,
                'has_balcony': True,
            },
            {
                'title': 'Victorian Townhouse - Stockbridge',
                'address': '28 Hamilton Place, Stockbridge, Edinburgh EH3 5AX',
                'price': 495000,
                'bedrooms': 3,
                'bathrooms': 2,
                'sqft': 1400,
                'property_type': 'house',
                'year': 1885,
                'refit_year': 2018,
                'parking_spaces': 2,
                'reception_rooms': 2,
                'energy_rating': 'D',
                'has_garden': True,
                'has_balcony': False,
            },
            {
                'title': 'Contemporary Flat - Newtown',
                'address': '15 Forrest Road, Newtown, Edinburgh EH1 3BX',
                'price': 275000,
                'bedrooms': 1,
                'bathrooms': 1,
                'sqft': 620,
                'property_type': 'apartment',
                'year': 2010,
                'parking_spaces': 0,
                'reception_rooms': 1,
                'energy_rating': 'B',
                'has_garden': False,
                'has_balcony': True,
            },
            {
                'title': 'Family Home with Garden - Murrayfield',
                'address': '56 Corstorphine Road, Murrayfield, Edinburgh EH12 6DD',
                'price': 650000,
                'bedrooms': 4,
                'bathrooms': 2,
                'sqft': 1800,
                'property_type': 'house',
                'year': 1995,
                'parking_spaces': 2,
                'reception_rooms': 3,
                'energy_rating': 'E',
                'has_garden': True,
                'has_balcony': False,
            },
            {
                'title': 'Spacious Two-Bedroom - Marchmont',
                'address': '78 Warrender Park Road, Marchmont, Edinburgh EH9 1DX',
                'price': 385000,
                'bedrooms': 2,
                'bathrooms': 2,
                'sqft': 950,
                'property_type': 'flat',
                'year': 1925,
                'refit_year': 2017,
                'parking_spaces': 1,
                'reception_rooms': 1,
                'energy_rating': 'D',
                'has_garden': False,
                'has_balcony': False,
            },
            {
                'title': 'Luxury Penthouse - New Town',
                'address': '99 George Street, New Town, Edinburgh EH2 3ES',
                'price': 850000,
                'bedrooms': 3,
                'bathrooms': 3,
                'sqft': 1600,
                'property_type': 'apartment',
                'year': 2020,
                'parking_spaces': 2,
                'reception_rooms': 2,
                'energy_rating': 'A',
                'has_garden': False,
                'has_balcony': True,
            },
        ]

        created_count = 0
        for prop_data in properties_data:
            # Check if property already exists
            if PropertyPage.objects.filter(title=prop_data['title']).exists():
                self.stdout.write(f"Property '{prop_data['title']}' already exists. Skipping.")
                continue

            # Create the property page
            page = PropertyPage(
                title=prop_data['title'],
                slug=prop_data['title'].lower().replace(' ', '-').replace("'", ''),
                address=prop_data['address'],
                price=prop_data['price'],
                bedrooms=prop_data['bedrooms'],
                bathrooms=prop_data['bathrooms'],
                sqft=prop_data['sqft'],
                property_type=prop_data['property_type'],
                year=prop_data.get('year'),
                refit_year=prop_data.get('refit_year'),
                parking_spaces=prop_data.get('parking_spaces'),
                reception_rooms=prop_data.get('reception_rooms'),
                energy_rating=prop_data.get('energy_rating'),
                has_garden=prop_data.get('has_garden', False),
                has_balcony=prop_data.get('has_balcony', False),
            )

            # Add as child to PropertyIndexPage
            index_page.add_child(instance=page)
            page.save_revision().publish()

            self.stdout.write(
                self.style.SUCCESS(f"✓ Created property: '{prop_data['title']}' (£{prop_data['price']:,})")
            )
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} test properties!')
        )
