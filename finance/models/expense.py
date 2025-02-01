from django.db import models

class Expense(models.Model):
    EXPENSE_CATEGORIES = (
        ('supplies', 'Supplies'),
        ('salaries', 'Salaries'),
        ('utilities', 'Utilities'),
        ('maintenance', 'Maintenance'),
        ('marketing', 'Marketing'),
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES)
    date = models.DateField(auto_now_add=True) 
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'expenses' 

    def __str__(self):
        return f"{self.category} - {self.amount} on {self.date.strftime('%Y-%m-%d')}"
