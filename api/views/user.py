from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from api.models.customer import Customer
from api.models.serializers import CustomerSerializer
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from api.common import validateUser
import jwt, datetime
import math
import random
import os
import shutil


# Register - Get mobileNumber, password, name, email and save it
@api_view(['POST'])
def RegisterView(request):
    try:
        serializer = CustomerSerializer(data=request.data)
    except Exception as e:
        return Response({"error": e.args}, status=500)  
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=200)
    
    return Response({"error": serializer.errors }, status=400)

# Login - Get mobileNumber, password then validate and set jwt token in cookies
@api_view(['POST'])
def LoginView(request):
    mobileNumber = request.data['mobileNumber']
    password = request.data['password']
    
    user = Customer.objects.filter(mobileNumber=mobileNumber).first()
    
    # user = Customer.objects.filter(mobileNumber=mobileNumber).first() 

    if user is None:
        raise AuthenticationFailed('User not found!')

    if not user.check_password(password):
        raise AuthenticationFailed('The username or passwrod is incorrect')
    
    if not user.isMobileNumberVerified:
        raise AuthenticationFailed('Please verify Mobile Number and proceed!')
    
    user.last_login = datetime.datetime.now()
    user.save()

    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60*24*30), # expiry time is 1month
        'iat': datetime.datetime.utcnow()
    }

    # token expire time 1hour
    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'user': user.id,
        'message': 'Successfully Loggedin!'
    }
    return response


@api_view(['POST'])
def SocialLoginView(request):
    email = request.data['email']
    provider = request.data['provider'] 
    
    user = Customer.objects.get(email=email, provider=provider)
    
    if user is None:
        raise AuthenticationFailed('User not found!')
    
    user.last_login = datetime.datetime.now()
    user.save()

    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60*24*30),
        'iat': datetime.datetime.utcnow()
    }

    # token expire time 1hour
    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'user': user.id,
        'message': 'Successfully Loggedin!'
    }
    return response


# Forget Password - Get mobileNumber then validate and send otp
@api_view(['PUT'])
def GetOtp(request, pk):
    mobileNumber = request.data['mobileNumber']
    user = Customer.objects.get(id = pk)

    if user is None:
        raise AuthenticationFailed('User not found!')

    try:
        user.mobileNumber = mobileNumber
        user.save()
        otp = math.floor(100000 + random.random() * 900000)
        print(otp)
        response = Response()
        response.data = {"otp": otp}
        return response
    except Exception as e:
        return Response({"error": e.args}, status=500)  

    return Response({"error": serializer.errors }, status=400)
    
    

# Forget Password - Get mobileNumber then validate and send otp
@api_view(['POST'])
def ForgetPassword(request):
    mobileNumber = request.data['mobileNumber']
    user = Customer.objects.filter(mobileNumber=mobileNumber).first()

    if user is None:
        raise AuthenticationFailed('User not found!')
    
    otp = math.floor(100000 + random.random() * 900000)
    print(otp)
    response = Response()
    response.data = {
        'otp': otp
    }

    return response


# Verirfy Mobile Number - Get otp then set isMobileNumberVerified = true
@api_view(['PUT'])
def VerifyMobileNumber(request):
    mobileNumber = request.data['mobileNumber']
    isOtpMatched = request.data['isOtpMatched']
    user = Customer.objects.get(mobileNumber=mobileNumber)

    if user is None:
        raise AuthenticationFailed('User not found!')
    
    user.isMobileNumberVerified = isOtpMatched
    user.save()
    response = Response()
    if user.provider == 'oauth':
        response.data = {
            'message': 'Mobile Number Successfully Verified!' if isOtpMatched else 'Wrong OTP!, Mobile Number verification failed.'
        }
    else:
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60*24*30),
            'iat': datetime.datetime.utcnow()
        }

        # token expire time 1hour
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'user': user,
            'message': 'Successfully Loggedin!'
        }
    return response


# User Profile - Get and Validate the jwt token from cookie then fetch specific user info
@api_view(['GET'])
def UserProfileView(request):
    valid_user_id = validateUser(request)
    user = Customer.objects.filter(id=valid_user_id).first()
    # user.profilePic = request.META['HTTP_HOST'] = user.profilePic
    serializer = CustomerSerializer(user)
    return Response(serializer.data)


# Update Profile - Get and Validate the jwt token from cookie then update specific user info
@api_view(['PUT'])
def UpdateUserInfo(request):
    valid_user_id = validateUser(request)
    user = Customer.objects.get(id=valid_user_id)
    user.name = request.data['name']
    user.email = request.data['email']
    user.save()
    
    response = Response()
    response.data = {
        'message': 'User info updated'
    }
    return response


# Change Password - Get and Validate the jwt token from cookie then validate old password and update new password
@api_view(['PUT'])
def ChangePassword(request):
    valid_user_id = validateUser(request)
    
    oldpassword = request.data['oldPassword']
    newpassword = request.data['newPassword']
    olduser = Customer.objects.filter(id=valid_user_id).first()
    
    if olduser is None:
        raise AuthenticationFailed('User not found!')

    if not olduser.check_password(oldpassword):
        raise AuthenticationFailed('Incorrect password!')

    user = Customer.objects.get(id=valid_user_id)
    user.password = make_password(newpassword)
    user.save()
    
    response = Response()
    response.data = {
        'message': 'Password changed successfully!'
    }
    return response


# Update Profile - Get and Validate the jwt token from cookie then update specific user profilepic
@api_view(['PUT'])
def UpdateProfilePic(request):
    valid_user_id = validateUser(request)
    
    olduser = Customer.objects.filter(id=valid_user_id).first()
    path = 'media/' + str(olduser.profilePic)
    if os.path.isdir(path):
        shutil.rmtree(path) 

    user = Customer.objects.get(id=valid_user_id)
    user.profilePic = request.data['profilePic']
    user.save()
    
    response = Response()
    response.data = {
        'message': 'Profile picture updated!'
    }
    return response