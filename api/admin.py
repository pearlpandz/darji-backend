from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models.customer import Customer
from api.models.company import Company
from api.models.category import Category
from api.models.property import Property, PropertyImage, PropertyVideo
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
        
class CompanyConfig(admin.ModelAdmin):
    exclude = []
    list_display = ['id','name','description','isVerified']
    search_fields=('name',)
    list_filter=('name',)
    # actions=[make_inactive,make_active]
    list_per_page = 10
    sortable_by=['id','name','isVerified']


class CategoryConfig(admin.ModelAdmin):
    exclude = []
    list_display = ['id','name','description','icon']
    search_fields=('name',)
    list_filter=('name',)
    # actions=[make_inactive,make_active]
    list_per_page = 10
    sortable_by=['id','name']

        
class ImagesInline(admin.StackedInline):
    model = PropertyImage
    extra = 0

class VideosInline(admin.StackedInline):
    model = PropertyVideo
    extra = 0

class PropertyConfig(admin.ModelAdmin):
    inlines = [ImagesInline, VideosInline]
    
    

admin.site.register(Customer, CustomerConfig)
admin.site.register(Company, CompanyConfig)
admin.site.register(Category, CategoryConfig)
admin.site.register(Property, PropertyConfig)
