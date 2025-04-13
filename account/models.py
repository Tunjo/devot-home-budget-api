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
        default=1000.00
    )

    def __str__(self):
        return f"{self.user.username}'s Budget: {self.budget}"
    
class BudgetHistory(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    CHANGE_TYPES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budget_history")
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    expense = models.ForeignKey('category.Expense', on_delete=models.SET_NULL, null=True, blank=True, related_name="budget_history")
    category = models.ForeignKey('category.Category', on_delete=models.SET_NULL, null=True, blank=True, related_name="budget_history")

    def __str__(self):
        return f"{self.user.username} - {self.change_type} - {self.amount} on {self.date}"


@receiver(post_save, sender=User)
def create_account_budget(instance, created, **kwargs):
    if created:
      account_budget = AccountBudget.objects.create(user=instance)

      BudgetHistory.objects.create(
          user=instance,
          change_type=BudgetHistory.INCOME,
          amount=account_budget.budget,
          description="Initial budget allocation",
      )




