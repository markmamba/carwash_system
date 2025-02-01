from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from services.models.booking import Booking
from services.serializers.booking import BookingSerializer
from users.models.users import User

class BookingList(generics.ListCreateAPIView):
    """View to list and create bookings."""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(is_deleted=False)
    
    def perform_create(self, serializer):
        user_id = self.request.data.get('user')
        staff_id = self.request.data.get('staff')
        
        if not user_id or not staff_id:
            raise ValidationError("Both User ID and Staff ID must be provided.")
        
        try:
            user = User.objects.get(id=user_id)
            staff = User.objects.get(id=staff_id)
        except User.DoesNotExist:
            raise ValidationError("User or staff with the provided ID does not exist.")
        
        # Save the booking with the specified user and staff
        serializer.save(user=user, staff=staff)

class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(is_deleted=False)

    def perform_update(self, serializer):
        if 'status' in self.request.data:
            status = self.request.data.get('status')
            if status not in ['pending', 'completed', 'cancelled']:
                raise ValidationError("Invalid status value.")
            serializer.save(status=status) 
        else:
            user_id = self.request.data.get('user')
            staff_id = self.request.data.get('staff')

            if user_id and staff_id:
                try:
                    user = User.objects.get(id=user_id)
                    staff = User.objects.get(id=staff_id)
                    serializer.save(user=user, staff=staff)
                except User.DoesNotExist:
                    raise ValidationError("User or staff with the provided ID does not exist.")
            else:
                serializer.save()
            
    def perform_destroy(self, instance):
        instance.delete()
        
class DeletedBookingList(generics.ListAPIView):
    """View to list soft-deleted bookings."""
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(is_deleted=True)




