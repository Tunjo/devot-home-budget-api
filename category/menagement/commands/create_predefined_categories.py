from django.core.management.base import BaseCommand
from category.models import Category

PREDEFINED_CATEGORIES = [
    'Food & Groceries',
    'Transportation',
    'Rent & Utilities',
    'Healthcare',
    'Entertainment'
]

class Command(BaseCommand):
    help = 'Create predefined categories'

    def handle(self, *args, **kwargs):
        for category_name in PREDEFINED_CATEGORIES:
            category, created = Category.objects.get_or_create(name=category_name, user=None)
            if created and not category:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {category_name}'))