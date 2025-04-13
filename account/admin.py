from django.contrib import admin
from .models import (
    AccountBudget,
    BudgetHistory
)

admin.site.register(AccountBudget)
admin.site.register(BudgetHistory)