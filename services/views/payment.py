from decimal import Decimal
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from services.models.payment import Payment
from services.serializers.payment import PaymentSerializer
from services.models.booking import Booking
from users.models.users import User

class PaymentList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return payments that are not deleted
        return self.queryset.filter(is_deleted=False)

    def perform_create(self, serializer):
        booking_id = self.request.data.get('booking_id')
        user_id = self.request.data.get('user')
        staff_id = self.request.data.get('staff')
        total_payment = self.request.data.get('total_payment')

        if not booking_id:
            raise ValidationError("Booking ID must be provided.")
        
        if total_payment is None:
            raise ValidationError("Total payment must be provided.")

        try:
            booking = Booking.objects.get(id=booking_id)

            user = User.objects.get(id=user_id) if user_id else None
            staff = User.objects.get(id=staff_id) if staff_id else None
            
            total_payment = Decimal(total_payment)

            staff_payment_percentage = total_payment * Decimal(0.40)

            payment = serializer.save(
                user=user,
                booking=booking,
                staff=staff,
                staff_payment_percentage=staff_payment_percentage 
            )

            if 'status' in serializer.validated_data and serializer.validated_data['status'] == 'completed':
                booking.status = 'completed'
                booking.save()

        except Booking.DoesNotExist:
            raise ValidationError("Booking with the provided ID does not exist.")
        except User.DoesNotExist:
            raise ValidationError("Staff with the provided ID does not exist.")

class PaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
