from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReadyViewSet, AtpStockViewSet, IntransitViewSet,
    ToBeProducedViewSet, SalesViewSet, UsersViewSet, ExcelUploadArchiveView,
    ReadyArchiveViewSet, AtpStockArchiveViewSet,
    IntransitArchiveViewSet, ToBeProducedArchiveViewSet,
    SalesArchiveViewSet, UpdatePalletInfoView,
    OptimizationRunView,
    GetTransportationInfo, ArchiveTransportationInfo, UpdateTransportationInfo

)

router = DefaultRouter()
router.register(r'ready', ReadyViewSet)
router.register(r'atp-stock', AtpStockViewSet)
router.register(r'intransit', IntransitViewSet)
router.register(r'to-be-produced', ToBeProducedViewSet)
router.register(r'sales', SalesViewSet)

router.register(r'users', UsersViewSet)

router.register(r'ready-archive', ReadyArchiveViewSet)
router.register(r'atp-stock-archive', AtpStockArchiveViewSet)
router.register(r'intransit-archive', IntransitArchiveViewSet)
router.register(r'to-be-produced-archive', ToBeProducedArchiveViewSet)
router.register(r'sales-archive', SalesArchiveViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('upload-table/', ExcelUploadArchiveView.as_view(), name='upload-table'),
    path('update_pallet_info/', UpdatePalletInfoView.as_view(), name='update-pallet-info'),
    path('optimize/', OptimizationRunView.as_view(), name='optimize'),
    path('transportation/', GetTransportationInfo.as_view()),
    path('transportation/archive/', ArchiveTransportationInfo.as_view()),
    path('transportation/update/', UpdateTransportationInfo.as_view()),
]
