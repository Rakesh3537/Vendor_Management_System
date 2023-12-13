# vendor_management_main/urls.py

from django.urls import path
from .views import(
    VendorListCreateView,
    VendorDetailView,
    PurchaseOrderListCreateView,
    PurchaseOrderDetailView,
    VendorPerformanceView,
    PurchaseOrderAcknowledgmentView,
    VendorHistoricalPerformanceView,
    VendorView
)


urlpatterns = [

    path('createVendor/', VendorListCreateView.as_view(), name='vendor_list_create_view'),
    path('vendors/', VendorListCreateView.as_view(), name='vendor_list_view'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor_detail_view'),
    path('purchase_orders/', PurchaseOrderListCreateView.as_view(),
         name='purchase_order_list_create_view'),
    path('purchase_orders/<int:pk>/', PurchaseOrderDetailView.as_view(),
         name='purchase_order_detail_view'),
    path('vendors/<int:pk>/performance/',
         VendorPerformanceView.as_view(), name='vendor_performance_view'),
    path('purchase_orders/<int:pk>/acknowledge/',
         PurchaseOrderAcknowledgmentView.as_view(), name='purchase_order_acknowledge_view'),
    path('historical_performance/', VendorHistoricalPerformanceView.as_view(),
         name='historical_performance_view'),
]