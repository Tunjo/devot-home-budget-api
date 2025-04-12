from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Trigger signals for all User objects"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.WARNING("No users found to trigger signals."))
            return

        for user in users:
            user.save()