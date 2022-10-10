from django.urls import path
from .views.user import *
from .views.company import *
from .views.category import *
from .views.property import *
from .views.favourite import *

# URL Configuration
urlpatterns = [

    # Auth
    path('login', LoginView),
    path('register', RegisterView),
    path('forgetpassword', ForgetPassword),
    path('verifyMobileNumber', VerifyMobileNumber),

    # User 
    path('profile', UserProfileView),
    path('updateinfo', UpdateUserInfo),
    path('updateprofilepic', UpdateProfilePic),
    path('changepassword', ChangePassword),

    # Company
    path('companies', get_companies),
    path('company', addCompany),
    path('company/<str:pk>', CompanyView),

    # Global Category
    path('categories', getCategories),
    path('category', addGlobalCategory),
    path('category/<str:pk>', globalCategoryView),

    # Property
    path('properties', getProperties),
    path('property/<str:pk>', PropertyView),

    # Favourite
    path('favourites', getAllFavourites),
    path('favourite', addToFavourite),
    path('favourite/<str:pk>', RemovePropertyFromFavourites)

]
