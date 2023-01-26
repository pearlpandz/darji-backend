from django.db import models
import os

class Pincode(models.Model):
    pincode = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    REQUIRED_FIELDS = ['name','pincode']

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return str(self.name)
