from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReadyViewSet

router = DefaultRouter()
router.register(r'ready', ReadyViewSet)  # Adjust name

urlpatterns = [
    path('', include(router.urls)),
]
