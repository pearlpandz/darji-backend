from django.db import models
from .customer import Customer

class Order(models.Model):
    gender = models.CharField(max_length=255, blank=True)
    orderType = models.CharField(max_length=255, blank=True)
    designType = models.CharField(max_length=255, blank=True)
    cloth_couriered = models.BooleanField(default=False)
    cloth_pickuplocation = models.TextField(blank=True)
    cloth_length = models.FloatField(default=0)
    cloth_total_price = models.FloatField(blank=True, default=0)
    cloth_id = models.IntegerField(blank=True, null=True)
    orderedDesign = models.JSONField(blank=True, null=True)
    measurements = models.JSONField(blank=True, null=True)
    deliveryAddress = models.TextField(blank=True)
    totalPrice = models.FloatField(blank=True, default=0)
    alreadyPaid = models.FloatField(blank=True, default=0)
    userId = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)

class ReferenceImage(models.Model):
    def get_image_path(instance, filename):
        return os.path.join('referenceImages', filename)

    url = models.ImageField(upload_to=get_image_path)
    orderId = models.ForeignKey(Order, default=None, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['url']

    def __str__(self):
        return self.url.url