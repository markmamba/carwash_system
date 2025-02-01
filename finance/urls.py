from django.urls import path
from finance.views.expense import ExpenseList, ExpenseDetail
from finance.views.finance_report import FinancialReportView
from finance.views.staff_income_report import StaffIncomeReportView
from finance.views.bookings_report import CompletedBookingsView

urlpatterns = [
    path('expenses/', ExpenseList.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', ExpenseDetail.as_view(), name='expense-detail'),
    
    path('finance/report/', FinancialReportView.as_view(), name='finance-report'),
    path('finance/staff-income-report/', StaffIncomeReportView.as_view(), name='staff-income-report'),
    path('completed-bookings/', CompletedBookingsView.as_view(), name='completed-bookings'),
]
