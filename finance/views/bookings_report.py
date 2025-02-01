from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from services.models.booking import Booking

class CompletedBookingsView(APIView):
    """
    View to get the all-time total number of completed bookings.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        total_completed_bookings = self.get_all_time_completed_bookings()
        weekly_completed_bookings = self.get_weekly_completed_bookings()
        monthly_completed_bookings = self.get_monthly_completed_bookings()
        
        return Response({
            "total_completed_bookings": total_completed_bookings,
            "weekly_completed_bookings": weekly_completed_bookings,
            "monthly_completed_bookings": monthly_completed_bookings,
        }, status=status.HTTP_200_OK)

    def get_all_time_completed_bookings(self):
        """Fetch the total count of all completed bookings."""
        return Booking.objects.filter(status='completed').count()

    def get_weekly_completed_bookings(self):
        """Fetch the total count of completed bookings for the current week."""
        today = timezone.now()
        start_of_week = today - timedelta(days=today.weekday())
        return Booking.objects.filter(status='completed', booking_date__date__gte=start_of_week.date()).count()

    def get_monthly_completed_bookings(self):
        """Fetch the total count of completed bookings for the current month."""
        today = timezone.now()
        start_of_month = today.replace(day=1)
        return Booking.objects.filter(status='completed', booking_date__date__gte=start_of_month.date()).count()
