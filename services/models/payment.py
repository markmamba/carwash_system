from django.db import models
from users.models.users import User
from rent.models.rent import Rental
from services.models.booking import Booking
from django.utils import timezone

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('gcash', 'G-Cash'),
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ], default='pending')
    remarks = models.TextField(blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    booking = models.OneToOneField(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment')
    rental = models.ForeignKey(Rental, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')

    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_payments')
    staff_payment_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Store staff payment percentage

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'payments' 

    def __str__(self):
        return f"Payment of {self.total_payment} by {self.user.username} on {self.payment_date.strftime('%Y-%m-%d %H:%M')}"

    @property
    def staff_earnings(self):
        """Calculate the staff's earnings based on the total payment and staff percentage."""
        return self.total_payment * self.staff_payment_percentage

    def delete(self, using=None, keep_parents=False):
        """Soft delete the payment instance."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

