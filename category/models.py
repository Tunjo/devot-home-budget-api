from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import (
    post_save,
    post_delete,
    pre_save
)
from django.dispatch import receiver
from account.contrib.unique_none import get_unique_or_none
from account.models import AccountBudget, BudgetHistory


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
    


@receiver(pre_save, sender=Expense)
def cache_previous_expense_state(sender, instance, **kwargs):
    """
    Cache the previous state of the Expense object before it is updated.
    """
    if instance.pk:
        try:
            instance._previous_state = Expense.objects.get(pk=instance.pk)
        except Expense.DoesNotExist:
            instance._previous_state = None
    

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
        budget.save()

        BudgetHistory.objects.create(
            user=instance.user,
            change_type=BudgetHistory.EXPENSE,
            amount=instance.amount,
            description=f'Expense created: {instance.description}',
            expense=instance,
            category=instance.category
        )

    else:
        previous_expense = getattr(instance, '_previous_state', None)
        if previous_expense:
            difference = previous_expense.amount - instance.amount

            if difference > 0:
                budget.budget += difference
                BudgetHistory.objects.create(
                    user=instance.user,
                    change_type=BudgetHistory.INCOME,
                    amount=difference,
                    description=f'Expense updated (difference treated as income): {instance.description}',
                    expense=instance,
                    category=instance.category
                )
            elif difference < 0:
                budget.budget += difference
                BudgetHistory.objects.create(
                    user=instance.user,
                    change_type=BudgetHistory.EXPENSE,
                    amount=abs(difference),
                    description=f'Expense updated (additional expense): {instance.description}',
                    expense=instance,
                    category=instance.category
                )

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

    BudgetHistory.objects.create(
        user=instance.user,
        change_type=BudgetHistory.INCOME,
        amount=instance.amount,
        description=f'Expense deleted: {instance.description}',
        expense=instance,
        category=instance.category
    )