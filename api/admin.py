from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models.customer import Customer
from api.models.cloth import Cloth
from api.models.order import Order, ReferenceImage
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

class ClothConfig(admin.ModelAdmin):
    exclude = []
    list_display = ['id','image','name','material','color','pricePermeter']
    search_fields=('name','material','color','pricePermeter')
    list_filter=('name','material','color','pricePermeter')
    # actions=[make_inactive,make_active]
    list_per_page = 10
    sortable_by=['id','name','material','color','pricePermeter']

class ImagesInline(admin.StackedInline):
    model = ReferenceImage
    extra = 0

class OrderConfig(admin.ModelAdmin):
    inlines = [ImagesInline]

admin.site.register(Customer, CustomerConfig)
admin.site.register(Cloth, ClothConfig)
admin.site.register(Order, OrderConfig)