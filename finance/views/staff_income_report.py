from decimal import Decimal
from rest_framework import views, response, status
from django.db.models import Sum, DecimalField, F, ExpressionWrapper
from django.utils import timezone
from services.models.payment import Payment
from django.db.models.functions import Coalesce

class StaffIncomeReportView(views.APIView):

    def get(self, request):
        # Extract query parameters
        specific_year = request.query_params.get('year')
        specific_month = request.query_params.get('month')
        staff_name = request.query_params.get('staff_name', None)

        # Retrieve total staff income and total cars washed
        total_staff_income, total_cars_washed = self.calculate_staff_income_and_cars_washed(
            specific_year, specific_month, staff_name
        )

        # Return the response
        return response.Response({
            'total_staff_income': total_staff_income,
            'total_cars_washed': total_cars_washed,
        }, status=status.HTTP_200_OK)

    def calculate_staff_income_and_cars_washed(self, specific_year, specific_month, staff_name):
        # Determine the date range based on the provided parameters
        start_date, end_date = self.get_date_range(specific_year, specific_month)

        # Filter the payment queryset based on the date range and staff name
        payment_queryset = self.get_filtered_payments(start_date, end_date, staff_name)

        # Calculate total staff income
        total_staff_income = self.aggregate_staff_income(payment_queryset)

        # Count total number of cars washed
        total_cars_washed = payment_queryset.count()

        return total_staff_income, total_cars_washed

    def get_date_range(self, specific_year, specific_month):
        """Get the start and end date based on the specified year and month."""
        if specific_year and specific_month:
            year = int(specific_year)
            month = int(specific_month)
            start_date = timezone.datetime(year=year, month=month, day=1)
            end_date = (start_date + timezone.timedelta(days=31)).replace(day=1) - timezone.timedelta(days=1)
        elif specific_year:
            year = int(specific_year)
            start_date = timezone.datetime(year=year, month=1, day=1)
            end_date = timezone.datetime(year=year, month=12, day=31)
        else:
            return None, None

        return start_date, end_date

    def get_filtered_payments(self, start_date, end_date, staff_name):
        """Filter the Payment queryset based on the date range and staff name."""
        payment_queryset = Payment.objects.all()

        if start_date and end_date:
            payment_queryset = payment_queryset.filter(payment_date__range=[start_date, end_date])
        if staff_name:
            payment_queryset = payment_queryset.filter(staff__name__icontains=staff_name)

        return payment_queryset

    def aggregate_staff_income(self, payment_queryset):
        """Calculate the total staff income from the payment queryset."""
        total_staff_income = payment_queryset.aggregate(
            total=Coalesce(
                Sum(
                    ExpressionWrapper(
                        F('staff_payment_percentage'),
                        output_field=DecimalField()  # Cast to DecimalField
                    ),
                    output_field=DecimalField()
                ),
                Decimal('0.00')  # Use Decimal for default value
            )
        )['total']

        # Return Decimal(0.00) if total_staff_income is None
        return total_staff_income if total_staff_income is not None else Decimal('0.00')
