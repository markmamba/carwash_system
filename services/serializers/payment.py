from rest_framework import serializers
from services.models.payment import Payment
from users.serializer.users import UserSerializer

class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    staff = UserSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_method', 'total_payment', 'status', 'remarks', 
                  'payment_date', 'booking', 'rental', 'staff', 'staff_payment_percentage', 
                  'is_deleted', 'deleted_at']
