from django.db import models
from .customer import Customer
import os

STATUS = (
    ('draft', 'Draft'),
    ('complete', 'Complete'),
)

PAYMENT_STATUS = (
    ('pending', 'pending'),
    ('partial', 'Partially Completed'),
    ('complete', 'complete'),
)

class Order(models.Model):
    userId = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    gender = models.CharField(max_length=255, blank=True)
    orderType = models.CharField(max_length=255, blank=True)
    designType = models.CharField(max_length=255, blank=True)
    
    cloth_id = models.IntegerField(blank=True, null=True)
    cloth_length = models.FloatField(default=0)
    cloth_total_price = models.FloatField(blank=True, default=0)
    cloth_couriered = models.BooleanField(default=False)
    cloth_pickuplocation = models.TextField(blank=True)
    
    orderedDesign = models.JSONField(blank=True, null=True)
    
    measurements = models.JSONField(blank=True, null=True)
    measurementAddress = models.TextField(blank=True)

    totalPrice = models.FloatField(blank=True, default=0)
    alreadyPaid = models.FloatField(blank=True, default=0)
    
    orderDate = models.DateTimeField(auto_now=True)
    orderStatus = models.CharField(max_length=255, choices=STATUS, default='draft')
    
    orderPaymentStatus = models.CharField(max_length=255, choices=PAYMENT_STATUS, default='pending')
    orderDeliveryDate = models.DateTimeField(null=True)
    deliveryAddress = models.TextField(blank=True)
    orderDeliveryStatus = models.CharField(max_length=255, choices=PAYMENT_STATUS, default='pending')

    razorpayPaymentId = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.razorpayPaymentId}'

class ReferenceImage(models.Model):
    def get_image_path(instance, filename):
        return os.path.join('referenceImages', filename)

    url = models.ImageField(upload_to=get_image_path)
    orderId = models.ForeignKey(Order, default=None, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['url']

    def __str__(self):
        return f'{self.url}'