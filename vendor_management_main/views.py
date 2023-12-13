from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from django.views import View

# Decorator to enforce login for HTML views
#login_required_decorator = method_decorator(login_required)

class MySecuredView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'This is a secured view!'})

#@method_decorator(login_required, name='dispatch')
class VendorView(View):
    def get(self, request, *args, **kwargs):
        vendors = Vendor.objects.all()
        return render(request, 'vendors.html', {'vendors': vendors})

#@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

class PurchaseOrderAcknowledgmentView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.acknowledgment_date = timezone.now()
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class VendorHistoricalPerformanceView(generics.ListCreateAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
