from rest_framework import viewsets
from .models import (
    Ready, AtpStock, Intransit, ToBeProduced, Sales, Users
)
from .serializers import (
    ReadySerializer, AtpStockSerializer, IntransitSerializer,
    ToBeProducedSerializer, SalesSerializer, UsersSerializer
)

def create_viewset(model, serializer):
    class GenericViewSet(viewsets.ModelViewSet):
        queryset = model.objects.all()
        serializer_class = serializer
    return GenericViewSet

ReadyViewSet = create_viewset(Ready, ReadySerializer)
AtpStockViewSet = create_viewset(AtpStock, AtpStockSerializer)
IntransitViewSet = create_viewset(Intransit, IntransitSerializer)
ToBeProducedViewSet = create_viewset(ToBeProduced, ToBeProducedSerializer)
SalesViewSet = create_viewset(Sales, SalesSerializer)
UsersViewSet = create_viewset(Users, UsersSerializer)