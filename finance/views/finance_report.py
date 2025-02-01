from rest_framework import views, response, status
from django.db.models import Sum
from django.utils import timezone
from finance.models.expense import Expense
from services.models.payment import Payment
from services.models.booking import Booking

class FinancialReportView(views.APIView):
    def get(self, request):
        filter_value = request.query_params.get('filter[value]', 'month')
        specific_year = request.query_params.get('year', None)

        if filter_value == 'month':
            monthly_income, monthly_expenses, monthly_labels = self.get_monthly_data()
            net_income = {label: income - expense for label, income, expense in zip(monthly_labels, monthly_income, monthly_expenses)}
            monthly_income_dict = {label: income for label, income in zip(monthly_labels, monthly_income)}
            monthly_expenses_dict = {label: expense for label, expense in zip(monthly_labels, monthly_expenses)}

            return response.Response({
                'monthly_income': monthly_income_dict,
                'monthly_expenses': monthly_expenses_dict,
                'net_income': net_income,
            }, status=status.HTTP_200_OK)

        elif filter_value == 'year':
            yearly_income, yearly_expenses, yearly_labels = self.get_yearly_data(specific_year)
            net_income = {label: income - expense for label, income, expense in zip(yearly_labels, yearly_income, yearly_expenses)}

            return response.Response({
                'yearly_income': {label: income for label, income in zip(yearly_labels, yearly_income)},
                'yearly_expenses': {label: expense for label, expense in zip(yearly_labels, yearly_expenses)},
                'net_income': net_income,
            }, status=status.HTTP_200_OK)
        
        elif filter_value == 'week':
            specific_year = request.query_params.get('year')
            weekly_income, weekly_expenses, net_income = self.get_weekly_data(specific_year)

            return response.Response({
                'weekly_income': weekly_income,
                'weekly_expenses': weekly_expenses,
                'net_income': net_income,
            }, status=status.HTTP_200_OK)

        else:
            start_date, end_date = self.get_date_range(filter_value)
            total_income = Payment.objects.filter(payment_date__range=[start_date, end_date]).aggregate(total=Sum('total_payment'))['total'] or 0
            total_expenses = Expense.objects.filter(date__range=[start_date, end_date]).aggregate(total=Sum('amount'))['total'] or 0

            return response.Response({
                'total_income': total_income,
                'total_expenses': total_expenses,
                'net_income': total_income - total_expenses,
            }, status=status.HTTP_200_OK)

    def get_date_range(self, filter_value):
        today = timezone.now()

        if filter_value == 'week':
            start_date = today - timezone.timedelta(days=today.weekday())
            end_date = start_date + timezone.timedelta(days=6)
        elif filter_value == 'month':
            start_date = today.replace(day=1)
            end_date = (start_date + timezone.timedelta(days=31)).replace(day=1) - timezone.timedelta(days=1)
        elif filter_value == 'year':
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
        else:
            raise ValueError("Invalid filter type")

        return start_date, end_date

    def get_monthly_data(self):
        today = timezone.now()
        current_year = today.year

        monthly_income = [0] * 12
        monthly_expenses = [0] * 12
        monthly_labels = [
            "January", "February", "March", "April", "May", "June", 
            "July", "August", "September", "October", "November", "December"
        ]

        income_data = Payment.objects.filter(payment_date__year=current_year).values('payment_date__month').annotate(total=Sum('total_payment'))
        for entry in income_data:
            month_index = entry['payment_date__month'] - 1  
            monthly_income[month_index] = entry['total'] or 0

        expense_data = Expense.objects.filter(date__year=current_year).values('date__month').annotate(total=Sum('amount'))
        for entry in expense_data:
            month_index = entry['date__month'] - 1  
            monthly_expenses[month_index] = entry['total'] or 0

        return monthly_income, monthly_expenses, monthly_labels

    def get_yearly_data(self, specific_year):
        today = timezone.now()
        current_year = today.year

        try:
            specific_year = int(specific_year) if specific_year else current_year
        except ValueError:
            specific_year = current_year 

        start_year = specific_year - 5
        end_year = specific_year + 5

        yearly_income = {year: 0 for year in range(start_year, end_year + 1)}
        yearly_expenses = {year: 0 for year in range(start_year, end_year + 1)}

        income_data = Payment.objects.filter(payment_date__year__gte=start_year, payment_date__year__lte=end_year).values('payment_date__year').annotate(total=Sum('total_payment'))
        for entry in income_data:
            yearly_income[entry['payment_date__year']] = entry['total'] or 0

        expense_data = Expense.objects.filter(date__year__gte=start_year, date__year__lte=end_year).values('date__year').annotate(total=Sum('amount'))
        for entry in expense_data:
            yearly_expenses[entry['date__year']] = entry['total'] or 0

        return list(yearly_income.values()), list(yearly_expenses.values()), list(yearly_income.keys())
    
    def get_weekly_data(self, specific_year=None):
        today = timezone.now()
        year = specific_year or today.year

        weekly_income = {f"Week {i}": 0 for i in range(1, 53)}
        weekly_expenses = {f"Week {i}": 0 for i in range(1, 53)}

        income_data = Payment.objects.filter(payment_date__year=year).values('payment_date__week').annotate(total=Sum('total_payment'))
        for entry in income_data:
            weekly_income[f"Week {entry['payment_date__week']}"] = entry['total'] or 0

        expense_data = Expense.objects.filter(date__year=year).values('date__week').annotate(total=Sum('amount'))
        for entry in expense_data:
            weekly_expenses[f"Week {entry['date__week']}"] = entry['total'] or 0

        net_income = {week: weekly_income[week] - weekly_expenses[week] for week in weekly_income.keys()}

        return weekly_income, weekly_expenses, net_income
    

