from django.urls import path
from .views import *

urlpatterns =[
       path('vendors/', VendorProfile.as_view(), name='vendors-profile'),
       path('vendors/<int:vendor_id>/', VendorProfileManagement.as_view(), name='vendors-profile-management'),
       path('purchase_orders/', PurchaseOrderView.as_view(), name='purchse-order'),
       path('purchase_orders/<int:po_id>/', PurchaseOrderManagement.as_view(), name='purchase-order-management'),
       path('vendors/<int:vendor_id>/performance/', HistorialPerformanceView.as_view(), name='vendors-profile-management/performance'),
       path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgeView.as_view(), name='purchase_orders-acknowledge'),
    ]
