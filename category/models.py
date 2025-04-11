from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from account.contrib.unique_none import get_unique_or_none
from account.models import AccountBudget


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='categories')

    class Meta:
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')

    def __str__(self):
        return f'{self.amount} - {self.category.name}'
    

@receiver(post_save, sender=Expense)
def update_budget_on_save(instance, created, **kwargs):
    """
    Adjust the user's budget when an expense is created or updated.
    """
    budget = get_unique_or_none(AccountBudget, user=instance.user)
    if budget is None:
        raise ValueError(f'AccountBudget not found for user {instance.user}')

    if created:
        budget.budget -= instance.amount
    else:
        previous_expense = get_unique_or_none(Expense, id=instance.id)
        if previous_expense is None:
            raise ValueError(f'Expense not found for id {instance.id}')
        budget.budget += previous_expense.amount
        budget.budget -= instance.amount

    budget.save()

@receiver(post_delete, sender=Expense)
def update_budget_on_delete(instance, **kwargs):
    """
    Return the expense amount to the user's budget when an expense is deleted.
    """
    budget = get_unique_or_none(AccountBudget, user=instance.user)
    if budget is None:
        raise ValueError(f'AccountBudget not found for user {instance.user}')
    budget.budget += instance.amount
    budget.save()