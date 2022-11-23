from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models.customer import Customer
from api.models.serializers import CustomerSerializer

# Register your models here.
class CustomerConfig(admin.ModelAdmin):
    exclude = ['last_login', 'isMobileNumberVerified', 'provider', 'password']
    list_display = ['id','name','mobileNumber','provider', 'email', 'gender', 'isMobileNumberVerified']
    search_fields=('name','email',)
    list_filter=('name','email',)
    # actions=[make_inactive,make_active]
    list_per_page = 25
    sortable_by=['id','name','provider']
    # raw_id_fields=['companyId']

admin.site.register(Customer, CustomerConfig)