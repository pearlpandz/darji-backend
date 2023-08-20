from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password
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
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, blank=True)
    mobile_number = models.CharField(max_length=255, unique=True, blank=True, null=True)
    otp = models.CharField(max_length=255, blank=True, null=True)
    is_mobile_number_verified = models.BooleanField(default=False)
    user_type = models.CharField(max_length=255, default='customer', choices=USERTYPE)
    provider = models.CharField(max_length=255, choices=PROVIDERS, default='oauth')
   
    profilePic = models.ImageField(
        null=True, blank=True, upload_to=get_profile_image_path)
    gender = models.CharField(max_length=255, blank=True)
    last_login = models.DateTimeField(auto_now_add=True)
    username = None

    def save(self, *args, **kwargs):
        if (self.password):
            self.password = make_password(self.password)
        super(Customer, self).save(*args, **kwargs)

    REQUIRED_FIELDS = ['name', 'usertype','email']
    USERNAME_FIELD = 'mobileNumber'

    def __str__(self):
        return f'{self.name}'


class Address(models.Model):
    type = models.CharField(max_length=255)
    house_number= models.CharField(max_length=255)
    street = models.CharField(max_length=100)
    area_name = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=20)
    landmark= models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.id}'
