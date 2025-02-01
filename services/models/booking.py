from django.db import models
from users.models.users import User
from django.utils import timezone

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')  
    total_payment = models.DecimalField(max_digits=10, decimal_places=2)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_bookings')  
    remarks = models.TextField(blank=True)
    booking_date = models.DateTimeField(auto_now_add=True) 
    service_type = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], default='pending')
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    class Meta:
        db_table = 'bookings' 
        managed = True

    def __str__(self):
        return f"Booking by {self.user.username} on {self.booking_date.strftime('%Y-%m-%d %H:%M')}"
