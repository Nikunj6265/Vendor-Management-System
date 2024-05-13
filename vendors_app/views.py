from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Q, F
from datetime import datetime
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Vendor Profile API view
class VendorProfile(APIView):
    # GET request to retrieve all vendors
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Retrieve all vendors
        vendor = Vendor.objects.all()
        # Serialize vendor data
        vendor_serializer = VendorSerializer(vendor, many=True)
        return Response(vendor_serializer.data)

    # POST request to create a new vendor
    def post(self, request):
        # Deserialize request data
        vendor_serializer = VendorSerializer(data=request.data)
        # Validate serializer data
        if vendor_serializer.is_valid():
            # Save valid vendor data
            vendor_serializer.save()
            return Response(vendor_serializer.data, status=status.HTTP_201_CREATED)
        return Response(vendor_serializer.errors)

# Vendor Profile Management API view
class VendorProfileManagement(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # GET request to retrieve a specific vendor's details
    def get(self, request, vendor_id):
        # Retrieve vendor by ID
        vendor = get_object_or_404(Vendor, id=vendor_id)
        # Serialize vendor data
        vendor_serializer = VendorSerializer(vendor)
        return Response(vendor_serializer.data)

    # DELETE request to delete a specific vendor
    def delete(self, request, vendor_id):
        # Retrieve vendor by ID
        vendor = get_object_or_404(Vendor, id=vendor_id)
        # Delete the vendor
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PUT request to update a specific vendor's details
    def put(self, request, vendor_id):
        # Retrieve vendor by ID
        vendor = get_object_or_404(Vendor, id=vendor_id)
        # Deserialize request data
        vendor_serializer = VendorSerializer(vendor, data=request.data)
        # Validate serializer data
        if vendor_serializer.is_valid():
            # Save valid vendor data
            vendor_serializer.save()
            return Response(vendor_serializer.data)
        return Response(vendor_serializer.errors)

# Purchase Order API view
class PurchaseOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # GET request to retrieve all purchase orders
    def get(self, request):
        # Get the vendor_id from the query parameters, if provided
        vendor_id = request.query_params.get('vendor_id')
        # If vendor_id is provided, filter purchase orders by vendor
        if vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor__id=vendor_id)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        # Serialize purchase order data
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    # POST request to create a new purchase order
    def post(self, request):
        # Deserialize request data
        order_serializer = PurchaseOrderSerializer(data=request.data)
        # Validate serializer data
        if order_serializer.is_valid():
            # Save valid purchase order data
            order_serializer.save()
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors)

# Purchase Order Management API view
class PurchaseOrderManagement(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # GET request to retrieve details of a specific purchase order
    def get(self, request, po_id):
        # Retrieve purchase order by ID
        order = get_object_or_404(PurchaseOrder, id=po_id)
        # Serialize purchase order data
        serializer = PurchaseOrderSerializer(order)
        return Response(serializer.data)

    # DELETE request to delete a specific purchase order
    def delete(self, request, po_id):
        # Retrieve purchase order by ID
        purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
        # Delete the purchase order
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PUT request to update a specific purchase order
    def put(self, request, po_id):
        # Retrieve purchase order by ID
        order = PurchaseOrder.objects.get(id=po_id)
        # Deserialize request data
        order_serializer = PurchaseOrderSerializer(order, data=request.data)
        # Validate serializer data
        if order_serializer.is_valid():
            # Save valid purchase order data
            order_serializer.save()
            return Response(order_serializer.data)
        return Response(order_serializer.errors)

# Historical Performance API view
class HistorialPerformanceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # GET request to retrieve historical performance metrics for a specific vendor
    def get(self, request, vendor_id):
        # Retrieve vendor by ID
        vendor = get_object_or_404(Vendor, id=vendor_id)
        # Calculate various performance metrics
        # On-Time Delivery Rate
        total_PO = PurchaseOrder.objects.filter(vendor__id=vendor_id).count()
        ontime_PO = PurchaseOrder.objects.filter(Q(vendor__id=vendor_id) & Q(status='completed') & Q(acknowledgment_date__lte=F('delivery_date'))).count()
        on_time_delivery_rate = ontime_PO / total_PO if total_PO != 0 else 0
        vendor.on_time_delivery_rate = on_time_delivery_rate

        # Calculate Quality Rating Average
        vendor_rating = PurchaseOrder.objects.filter(Q(vendor__id=vendor_id) & Q(status='completed'))
        total_completed_orders = vendor_rating.count()
        total_rating = sum([v.quality_rating for v in vendor_rating if v.quality_rating is not None])
        avg_quality_rating = total_rating / total_completed_orders if total_completed_orders != 0 else 0
        vendor.quality_rating_avg = avg_quality_rating

        # Calculate Average Response Time in Hours
        acknowledged_orders = PurchaseOrder.objects.filter(acknowledgment_date__isnull=False)
        total_acknowledge_orders = acknowledged_orders.count()
        order_response_time = sum([(t.acknowledgment_date.timestamp() - t.issue_date.timestamp()) for t in acknowledged_orders])
        # order_response_time is in seconds converting it into days by dividing it by 86400
        average_response_time = (order_response_time / total_acknowledge_orders) / 86400 if total_acknowledge_orders != 0 else 0
        vendor.average_response_time = average_response_time

        # Calculate Fulfilment Rate
        total_orders = PurchaseOrder.objects.filter(Q(vendor__id=vendor_id) & (Q(status='completed') | Q(status='canceled'))).count()
        fulfillment_rate = total_completed_orders / total_orders if total_orders != 0 else 0
        vendor.fulfillment_rate = fulfillment_rate
        vendor.save()

        vendor_metrics = HistoricalPerformance.objects.filter(vendor=vendor).first()
        # Check vendors HistoricalPerformance exists or not
        # Check if vendor_metrics exists
        if vendor_metrics:
            # vendor_metrics exists, update the details
            vendor_metrics.date = datetime.now()
            vendor_metrics.on_time_delivery_rate = on_time_delivery_rate
            vendor_metrics.quality_rating_avg = avg_quality_rating
            vendor_metrics.average_response_time = average_response_time
            vendor_metrics.fulfillment_rate = fulfillment_rate
            vendor_metrics.save()
        else:
            # Does not exist, create a new record
            vendor_metrics = HistoricalPerformance.objects.create(
                vendor=vendor,
                date=datetime.now(),
                on_time_delivery_rate=on_time_delivery_rate,
                quality_rating_avg=avg_quality_rating,
                average_response_time=average_response_time,
                fulfillment_rate=fulfillment_rate
            )
        serializer = HistoricalPerformanceSerializer(vendor_metrics)
        return Response(serializer.data)

# Acknowledge View API view
class AcknowledgeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # POST request to acknowledge a purchase order
    def post(self, request, po_id):
        # Retrieve purchase order by ID
        po = get_object_or_404(PurchaseOrder, id=po_id)
        # Update acknowledgment date
        po.acknowledgment_date = datetime.now()
        po.save()
        # Update vendor's average response time
        vendors = Vendor.objects.filter(purchase_orders__id=po_id).first()
        acknowledged_orders = PurchaseOrder.objects.filter(vendor__id=vendors.id)
        total_acknowledge_orders = acknowledged_orders.count()
        order_response_time = sum([(t.acknowledgment_date.timestamp() - t.issue_date.timestamp()) for t in acknowledged_orders])
        # order_response_time is in seconds converting it into days by dividing it by 86400
        average_response_time = (order_response_time / total_acknowledge_orders) / 86400 if total_acknowledge_orders != 0 else 0
        vendors.average_response_time = average_response_time
        vendors.save()
        return Response({"acknowledgement": "Successful"})
