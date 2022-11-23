from django.urls import path
from .views.user import *

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

]
