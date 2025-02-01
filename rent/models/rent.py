from django.db import models
from django.utils import timezone

class Rental(models.Model):
    renter_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ], default='pending')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Rental payment by {self.renter_name} - {self.status}"
