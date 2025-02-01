from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from services.models.service import Service
from services.serializers.service import ServiceSerializer

class ServiceList(generics.ListCreateAPIView):
    """View to list and create services."""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, and delete a service."""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated] 
