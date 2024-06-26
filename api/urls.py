from django.urls import path
from .views.user import *
from .views.cloth import *
from .views.order import *
from .views.pincode import *

# URL Configuration
urlpatterns = [

    # Auth
    path('isExisting', isExisting),
    path('login', LoginView),
    path('socialLogin', SocialLoginView),
    path('register', RegisterView),
    path('verifyMobileNumber', VerifyMobileNumber),
    path('forgetpassword', ForgetPassword),
    path('createpassword', createPassword),

    # User 
    path('profile', UserProfileView),
    path('updateinfo', UpdateUserInfo),
    path('updateprofilepic', UpdateProfilePic),
    path('changepassword', ChangePassword),
    path('address', AddAddress),
    path('addresses', ListAddress),

    # Company
    path('cloths', getItems),
    path('cloth', addItem),
    path('cloth/<str:pk>', singleItem),

    # Order
    path('orders', getOrderList),
    path('order', newOrder),
    path('order/<str:pk>', getSingleOrder),
    path('updateOrder/<str:pk>', updateOrder),
    path('orderReferenceImage/<str:pk>', orderReferenceImage),
    path('measurement', AddMeasurement),
    path('measurements', getMeasurementList),

    # Pincode
    path('pincodes', get_pincodes)
]
