from rest_framework import serializers
from rent.models.rent import Rental

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['id', 'renter_name', 'amount', 'payment_date', 'status', 'remarks']
