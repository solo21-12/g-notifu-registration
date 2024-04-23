from django.shortcuts import render
from rest_framework import viewsets
from .serializers import VehicleSerializer
from .models import Vehicel
# Create your views here.


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicel.objects.all()
    serializer_class = VehicleSerializer
