from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class AccountBudget(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='account_budget'
    )
    budget = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=500.00
    )

    def __str__(self):
        return f"{self.user.username}'s Budget: {self.budget}"

@receiver(post_save, sender=User)
def create_account_budget(instance, created, **kwargs):
    if created:
        AccountBudget.objects.create(user=instance)


