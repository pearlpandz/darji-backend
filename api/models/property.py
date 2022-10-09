from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from multiselectfield import MultiSelectField
from api.models.category import Category
# from api.models.propertyImage import PropertyImage
from datetime import datetime
import os


class Property(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    category = models.ManyToManyField(Category, blank=True)

    # images = models.ForeignKey(PropertyImage, blank=True,on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name


class PropertyImage(models.Model):
    def get_image_path(instance, filename):
        print(instance);
        return os.path.join('property', filename)

    url = models.ImageField(upload_to=get_image_path)
    product = models.ForeignKey(Property, default=None, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['url']

    def __str__(self):
        return self.url.url


class PropertyVideo(models.Model):

    youtubeUrl = models.CharField(max_length=255, blank=True)
    product = models.ForeignKey(Property, default=None, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['youtubeUrl']

    def __str__(self):
        return self.youtubeUrl