from django.urls import path
from .views.user import *
from .views.cloth import *
from .views.order import *

# URL Configuration
urlpatterns = [

    # Auth
    path('login', LoginView),
    path('sociallogin', SocialLoginView),
    path('register', RegisterView),
    path('forgetpassword', ForgetPassword),
    path('verifyMobileNumber', VerifyMobileNumber),

    # User 
    path('profile', UserProfileView),
    path('updateinfo', UpdateUserInfo),
    path('updateprofilepic', UpdateProfilePic),
    path('changepassword', ChangePassword),

    # Company
    path('cloths', getItems),
    path('cloth', addItem),
    path('cloth/<str:pk>', singleItem),

    # Order
    path('orders', getOrderList),
    path('order', newOrder),
    path('order/<str:pk>', getSingleOrder),
    path('updateOrder/<str:pk>', updateOrder),
    path('orderReferenceImage/<str:pk>', orderReferenceImage)
]
