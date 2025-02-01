# users/urls.py
from django.urls import path, include  # include is necessary to include router URLs
from rest_framework import routers
from users.view.users import UserViewSet, CustomerList, CustomerDetail, StaffDetail, StaffList

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)  # This handles both list and detail routes for users

urlpatterns = [
    path('', include(router.urls)),  # Include all the routes from the router
    path('customers/', CustomerList.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerDetail.as_view(), name='customer-detail'),
    path('staff/', StaffList.as_view(), name='staff-list'),
    path('staff/<int:pk>/', StaffDetail.as_view(), name='staff-detail'),  
]
