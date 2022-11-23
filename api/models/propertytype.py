from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from multiselectfield import MultiSelectField
from datetime import datetime
import os


class PropertyType(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
