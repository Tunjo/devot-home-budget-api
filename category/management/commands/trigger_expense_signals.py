from django.core.management.base import BaseCommand
from category.models import Expense

class Command(BaseCommand):
    help = "Trigger signals for all Expense objects"

    def handle(self, *args, **kwargs):
        expenses = Expense.objects.all()
        if not expenses.exists():
            self.stdout.write(self.style.WARNING("No expenses found to trigger signals."))
            return

        for expense in expenses:
            expense.save()