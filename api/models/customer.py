from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from multiselectfield import MultiSelectField
from api.models.company import Company
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
    ('owner', 'Owner'),
    ('broker', 'Broker')
)

MY_CHOICES = (('item_key1', 'Item title 1.1'),
              ('item_key2', 'Item title 1.2'),
              ('item_key3', 'Item title 1.3'),
              ('item_key4', 'Item title 1.4'),
              ('item_key5', 'Item title 1.5'))


class Customer(AbstractBaseUser, models.Model):
    name = models.CharField(max_length=255)
    usertype = models.CharField(
        max_length=255, default='customer', choices=USERTYPE)
    password = models.CharField(max_length=255)
    mobileNumber = models.CharField(max_length=255, unique=True)
    isMobileNumberVerified = models.BooleanField(default=False)
    email = models.CharField(max_length=255, blank=True)
    profilePic = models.ImageField(
        null=True, blank=True, upload_to=get_profile_image_path)
    provider = models.CharField(
        max_length=255, default='oauth', choices=PROVIDERS)
    provider1 = models.CharField(
        max_length=255, default='oauth', choices=PROVIDERS)
    # provider = MultiSelectField(choices=MY_CHOICES, max_choices=3)
    gender = models.CharField(max_length=255, blank=True)
    companyId = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.SET_NULL)
    last_login = models.DateTimeField(auto_now_add=True)
    username = None

    def save(self, *args, **kwargs):
        # self.isMobileNumberVerified = False if self.isMobileNumberVerified == 'false' else True
        super(Customer, self).save(*args, **kwargs)

    REQUIRED_FIELDS = ['name', 'usertype', 'password', 'mobileNumber']
    USERNAME_FIELD = 'mobileNumber'
