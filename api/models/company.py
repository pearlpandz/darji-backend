from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from multiselectfield import MultiSelectField
from datetime import datetime
import os


def get_company_image_path(instance, filename):
    return os.path.join('company', str(instance.id), filename)


class Company(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    isVerified = models.BooleanField(default=False)
    logo = models.ImageField(null=True, blank=True,
                             upload_to=get_company_image_path)
    banner = models.ImageField(
        null=True, blank=True, upload_to=get_company_image_path)
    # companyId = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL)

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
