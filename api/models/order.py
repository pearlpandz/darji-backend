from django.db import models
from .customer import Customer, Address
from .cloth import Cloth
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

class Measurement(models.Model):
    type = models.CharField(max_length=255, blank=True) # shirt/pant
    value = models.JSONField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    measurement_for = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.id}'

class Order(models.Model):
    userId = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    gender = models.CharField(max_length=255, blank=True)
    orderType = models.CharField(max_length=255, blank=True)
    designType = models.CharField(max_length=255, blank=True)
    
    cloth = models.ForeignKey(Cloth, null=True, on_delete=models.SET_NULL)
    cloth_length = models.FloatField(default=0)
    cloth_total_price = models.FloatField(blank=True, default=0)
    cloth_couriered = models.BooleanField(default=False)
    cloth_pickuplocation = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL, related_name='cloth_pickup_location')
    
    orderedDesign = models.JSONField(blank=True, null=True)
    
    measurementId = models.ForeignKey(Measurement, null=True, on_delete=models.SET_NULL)
    measurementAddress = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL, related_name='measurement_pickup_location')

    totalPrice = models.FloatField(blank=True, default=0)
    alreadyPaid = models.FloatField(blank=True, default=0)
    
    orderDate = models.DateTimeField(auto_now=True)
    orderStatus = models.CharField(max_length=255, choices=STATUS, default='draft')
    
    orderPaymentStatus = models.CharField(max_length=255, choices=PAYMENT_STATUS, default='pending')
    orderDeliveryDate = models.DateTimeField(null=True)
    deliveryAddress = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL, related_name='delivery_location')
    orderDeliveryStatus = models.CharField(max_length=255, choices=PAYMENT_STATUS, default='pending')

    razorpayPaymentId = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.razorpayPaymentId}'

class ReferenceImage(models.Model):
    def get_image_path(instance, filename):
        return os.path.join('referenceImages', filename)

    url = models.ImageField(upload_to=get_image_path)
    orderId = models.ForeignKey(Order, default=None, on_delete=models.SET_NULL, null=True)

    REQUIRED_FIELDS = ['url', 'orderId']

    def __str__(self):
        return f'{self.id}'