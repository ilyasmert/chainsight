from django.shortcuts import render
from rest_framework import viewsets
from .models import Ready
from .serializers import ReadySerializer

class ReadyViewSet(viewsets.ModelViewSet):
    queryset = Ready.objects.all()
    serializer_class = ReadySerializer

# Create your views here.
