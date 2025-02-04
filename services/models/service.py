from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'services' 

    def __str__(self):
        return self.name
