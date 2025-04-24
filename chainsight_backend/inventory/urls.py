from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReadyViewSet, AtpStockViewSet, IntransitViewSet,
    ToBeProducedViewSet, SalesViewSet, UsersViewSet, ExcelUploadArchiveView
)

router = DefaultRouter()
router.register(r'ready', ReadyViewSet)
router.register(r'atp-stock', AtpStockViewSet)
router.register(r'intransit', IntransitViewSet)
router.register(r'to-be-produced', ToBeProducedViewSet)
router.register(r'sales', SalesViewSet)
router.register(r'users', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-table/', ExcelUploadArchiveView.as_view(), name='upload-table'),
]
