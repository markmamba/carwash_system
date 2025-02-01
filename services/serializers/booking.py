from rest_framework import serializers
from services.models.booking import Booking
from users.serializer.users import UserSerializer
from services.serializers.payment import PaymentSerializer

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    staff = UserSerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'total_payment', 'staff', 'remarks', 'booking_date', 'service_type', 'status','payment']
        read_only_fields = ['booking_date']

