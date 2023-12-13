from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorManagementTests(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name="Test Vendor", vendor_code="V001",contact_details="test123@gmail.com",address="Test Address")
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            order_date="2023-12-13T00:00:00Z",
            delivery_date="2023-12-14T00:00:00Z",
            items="Smart Phone",
            quantity=10,
            status="Pending",
            quality_rating=10,

        )
        self.historical_performance = HistoricalPerformance.objects.create(
            vendor=self.vendor,
            date="2023-01-01T00:00:00Z",
            on_time_delivery_rate=0.95,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=0.98,
        )

        self.client = APIClient()

    def test_vendor_list_create_view(self):
        url = reverse("vendor_list_create_view")
        data = {"name": "New Vendor", "vendor_code": "V002","contact_details":"test123@gmail.com","address":"Test Address"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    def test_vendor_detail_view(self):
        url = reverse("vendor_detail_view", kwargs={"pk": self.vendor.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Vendor")

    def test_purchase_order_list_create_view(self):
        url = reverse("purchase_order_list_create_view")
        data = {
            "po_number": "PO002",
            "vendor": self.vendor.pk,
            "order_date": "2023-02-01T00:00:00Z",
            "delivery_date":"2023-12-14T00:00:00Z",
            "items":"Lap",
            "quantity": 5,
            "status": "Pending",
            "quality_rating":10,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    def test_purchase_order_detail_view(self):
        url = reverse("purchase_order_detail_view", kwargs={"pk": self.purchase_order.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["po_number"], "PO001")

    def test_vendor_historical_performance_view(self):
        url = reverse("historical_performance_view")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def tearDown(self):
        # Clean up the data after each test
        Vendor.objects.all().delete()
        PurchaseOrder.objects.all().delete()
        HistoricalPerformance.objects.all().delete()
