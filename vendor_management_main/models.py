from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db.models.signals import post_save
from django.dispatch import receiver

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=10, unique=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=True,editable=False)
    quality_rating_avg = models.FloatField(null=True, blank=True,editable=False)
    average_response_time = models.FloatField(null=True, blank=True,editable=False)
    fulfillment_rate = models.FloatField(null=True, blank=True,editable=False)


    def __str__(self):
        return f"{self.vendor_code} ({self.id})"


    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchase_order.filter(status__iexact='completed', delivery_date__lte=models.F('acknowledgment_date'))
        total_completed_pos = completed_pos.count()
        if total_completed_pos > 0:
            on_time_delivery_rate = completed_pos.filter(status__iexact='completed').count() / total_completed_pos
            self.on_time_delivery_rate = on_time_delivery_rate
        else:
            self.on_time_delivery_rate = None

    def calculate_quality_rating_avg(self):
        completed_pos = self.purchase_order.filter(status__iexact='completed').exclude(quality_rating__isnull=True)
        total_completed_pos = completed_pos.count()
        if total_completed_pos > 0:
            quality_rating_avg = completed_pos.aggregate(models.Avg('quality_rating'))['quality_rating__avg']
            self.quality_rating_avg = quality_rating_avg
        else:
            self.quality_rating_avg = None

    def calculate_average_response_time(self):
        completed_pos = self.purchase_order.filter(status__iexact='completed').exclude(acknowledgment_date__isnull=True)
        total_completed_pos = completed_pos.count()
        if total_completed_pos > 0:
            response_times = ((po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_pos)
            average_response_time = sum(response_times) / total_completed_pos
            self.average_response_time = average_response_time
        else:
            self.average_response_time = None

    def calculate_fulfillment_rate(self):
        total_pos = self.purchase_order.count()
        if total_pos > 0:
            fulfillment_rate = self.purchase_order.filter(status__iexact='completed').count() / total_pos
            self.fulfillment_rate = fulfillment_rate
        else:
            self.fulfillment_rate = None

    


class PurchaseOrder(models.Model):

    po_number = models.CharField(max_length=10, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_order')
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.CharField(max_length=5000)
    quantity = models.IntegerField()
    status = models.CharField(max_length=30)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def set_items(self, items):
        self.items = json.dumps(items, cls=DjangoJSONEncoder)

    def get_items(self):
        return json.loads(self.items)

    items_json = property(get_items, set_items)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.vendor.calculate_on_time_delivery_rate()
        self.vendor.calculate_quality_rating_avg()
        self.vendor.calculate_average_response_time()
        self.vendor.calculate_fulfillment_rate()
        self.vendor.save()

    
@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    vendor = instance.vendor

    vendor.calculate_on_time_delivery_rate()
    vendor.calculate_quality_rating_avg()
    vendor.calculate_average_response_time()
    vendor.calculate_fulfillment_rate()

    vendor.save()

class HistoricalPerformance(models.Model):

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()


