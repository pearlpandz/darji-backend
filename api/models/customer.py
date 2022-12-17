from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from multiselectfield import MultiSelectField
from datetime import datetime
import os

def get_profile_image_path(instance, filename):
    return os.path.join('profilepics', str(instance.id), filename)

PROVIDERS = (
    ('oauth', 'Oauth'),
    ('facebook', 'Facebook'),
    ('google', 'Google')
)

USERTYPE = (
    ('customer', 'Customer'),
    ('owner', 'Owner')
)

class Customer(AbstractBaseUser, models.Model):
    name = models.CharField(max_length=255)
    usertype = models.CharField(
        max_length=255, default='customer', choices=USERTYPE)
    password = models.CharField(max_length=255, blank=True)
    mobileNumber = models.CharField(max_length=255, unique=True, blank=True)
    isMobileNumberVerified = models.BooleanField(default=False)
    email = models.CharField(max_length=255, blank=True, unique=True)
    profilePic = models.ImageField(
        null=True, blank=True, upload_to=get_profile_image_path)
    provider = models.CharField(
        max_length=255, default='oauth', choices=PROVIDERS)
    gender = models.CharField(max_length=255, blank=True)
    last_login = models.DateTimeField(auto_now_add=True)
    username = None

    def save(self, *args, **kwargs):
        # self.isMobileNumberVerified = False if self.isMobileNumberVerified == 'false' else True
        super(Customer, self).save(*args, **kwargs)

    REQUIRED_FIELDS = ['name', 'usertype', 'password', 'mobileNumber']
    USERNAME_FIELD = 'mobileNumber'
