from django.urls import path
from rent.views.rent import RentalListCreateView, RentalDetailView

urlpatterns = [
    path('rentals/', RentalListCreateView.as_view(), name='rental-list-create'),
    path('rentals/<int:pk>/', RentalDetailView.as_view(), name='rental-detail'),
]
