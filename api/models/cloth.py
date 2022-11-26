from django.db import models
import os

class Cloth(models.Model):
    def get_image_path(instance, filename):
        return os.path.join('cloth', filename)

    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=get_image_path)
    material = models.CharField(max_length=255, blank=True)
    color = models.CharField(max_length=255, blank=True)
    pricePermeter = models.FloatField(default=0)

    REQUIRED_FIELDS = ['name','image','material','color']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
