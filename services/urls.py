from django.urls import path
from services.views.booking import BookingList, BookingDetail
from services.views.service import ServiceList, ServiceDetail
from services.views.payment import PaymentList, PaymentDetail  

urlpatterns = [
    path('bookings/', BookingList.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetail.as_view(), name='booking-detail'),
    path('services/', ServiceList.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceDetail.as_view(), name='service-detail'),
    path('payments/', PaymentList.as_view(), name='payment-list'),  
    path('payments/<int:pk>/', PaymentDetail.as_view(), name='payment-detail'),  
]

