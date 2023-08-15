from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed, NotAcceptable
from api.models.customer import Customer
from django.core.exceptions import ObjectDoesNotExist
from api.models.serializers import CustomerSerializer
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from api.common import validateUser
from rest_framework import status
import jwt, datetime
import math
import random
import os
import shutil
from utils.otp import sendOtp
from utils.token import get_tokens_for_user

@api_view(['POST'])
def isExisting(request):
    mobile_number = request.data.get("mobile_number")
    email = request.data.get("email")
    isExistingUser = False
    try:
        if mobile_number:
            user = Customer.objects.get(mobile_number=mobile_number)
        if email:
            user = Customer.objects.get(email=email)
        if user.mobile_number:
            isExistingUser = True
        else:
            isExistingUser = False
    except Customer.DoesNotExist:
        isExistingUser = False
    response = Response()
    response.data = {"isExisting": isExistingUser}
    response.status_code = status.HTTP_200_OK
    return response


# Register - Get name, email, password and save it - done
@api_view(['POST'])
def RegisterView(request):
    try:
        payload = request.data
        serializer = CustomerSerializer(data=payload)
        response = Response()
    except Exception as e:
        return Response({"error": e.args}, status=500)  
    if serializer.is_valid():
        serializer.save()

        mobile_number = request.data.get("mobile_number")
        otp = sendOtp(mobile_number)
        user = Customer.objects.filter(mobile_number=mobile_number)
        user.update(otp = otp) 
        response.data= {"message": "Registration successful, otp sent!"}
        response.status_code = status.HTTP_201_CREATED
        return response
    
    return Response({"error": serializer.errors }, status=400)

# Verirfy Mobile Number - Get otp then set is_mobile_number_verified = true - done
@api_view(['PUT'])
def VerifyMobileNumber(request):
    mobile_number = request.data['mobile_number']
    otp = request.data['otp']
    user = Customer.objects.get(mobile_number=mobile_number)
    userObj = Customer.objects.filter(mobile_number=mobile_number)
    try:
        response = Response()
        if user.otp == otp:
            userObj.update(otp = None, is_mobile_number_verified=True) 
        else:
            response.data = {
                'message': 'Wrong OTP!, Mobile Number verification failed.'
            }
            response.status_code = 400
            return response
        
    except:
        if user is None:
            raise AuthenticationFailed('User not found!')
    
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=60*24*30)
    userinfo = userObj.values()[0]
    del userinfo['password']
    del userinfo['otp']
    token = get_tokens_for_user(user)
    response.set_cookie(key='jwt', value=token['access'], httponly=True, samesite='None', secure=True)
    response.data = {
        'userinfo': userinfo,
        'message': 'Mobile Number Successfully Verified!',
        'token': token['access']
    }
    response.status_code = 200
    return response

# Login - Get mobile_number, password then validate and set jwt token in cookies - done
@api_view(['POST'])
def LoginView(request):
    mobile_number = request.data['mobile_number']
    password = request.data['password']
    
    userObj = Customer.objects.filter(mobile_number=mobile_number)
    user = userObj.first()

    if user is None:
        raise AuthenticationFailed('User not found!')

    if not user.check_password(password):
        raise AuthenticationFailed('The username or passwrod is incorrect')
    
    if not user.is_mobile_number_verified:
        raise AuthenticationFailed('Please verify Mobile Number and proceed!')
    
    userObj.update(last_login=datetime.datetime.now())

    token = get_tokens_for_user(user) 
    
    response = Response()
    response.set_cookie(key='jwt', value=token['access'], httponly=True, samesite='None', secure=True)

    userinfo = userObj.values()[0]
    del userinfo['password']
    del userinfo['otp']

    response.data = {
        'userinfo': userinfo,
        'message': 'Successfully Loggedin!',
        'token': token['access']
    }
    return response


@api_view(['POST'])
def SocialLoginView(request):
    email = request.data['email']
    provider = request.data['provider'] 
    print(email)
    try:
        userObj = Customer.objects.filter(email=email, provider=provider)
        user = userObj.first()
        userObj.update(last_login=datetime.datetime.now())    
        token = get_tokens_for_user(user)
        response = Response()
        response.set_cookie(key='jwt', value=token['access'], httponly=True, samesite='None', secure=True)
        userinfo = userObj.values()[0]
        del userinfo['password']
        del userinfo['otp']
        response.data = {
            'userinfo': userinfo,
            'message': 'Successfully Loggedin!',
            'token': token['access']
        }
        response.status_code = 200
        return response
    except:
        data = {
            'message': 'User not found'
        }
        return Response(data, status=404)


# Forget Password - Get mobile_number then validate and send otp
@api_view(['POST'])
def ForgetPassword(request):
    response = Response()
    mobile_number = request.data['mobile_number']
    try:
        user = Customer.objects.filter(mobile_number=mobile_number).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if user.provider != 'oauth':
            response.data = { "message": "Forget Password is not required for social accounts! Please continue with social login" }
            response.status_code = 400
            return response
        else:
            otp = sendOtp(mobile_number)
            userObj = Customer.objects.filter(mobile_number=mobile_number)
            userObj.update(otp = otp) 
            response.data= {"message": "otp sent for verificationt!"}
            response.status_code = 200
            return response
    except Exception as e:
        return Response({"error": e.args}, status=500)  

@api_view(['POST'])
def createPassword(request):
    valid_user_id = validateUser(request)
    password = request.data.get("password")
    if password:
        user = Customer.objects.filter(id=valid_user_id)
        user.update(password=make_password(password))
    else:
        raise NotAcceptable(detail="Empty password received")
    return Response({'message': 'Password set successfully!'}, status.HTTP_200_OK)


# Change Password - Get and Validate the jwt token from cookie then validate old password and update new password
@api_view(['PUT'])
def ChangePassword(request):
    valid_user_id = validateUser(request)
    
    oldpassword = request.data['oldPassword']
    newpassword = request.data['newPassword']

    user = Customer.objects.filter(id=valid_user_id)
    olduser = user.first()
    
    if olduser is None:
        raise AuthenticationFailed('User not found!')

    if not olduser.check_password(oldpassword):
        raise AuthenticationFailed({'error': 'Current password is incorrect!'})

    # user = Customer.objects.get(id=valid_user_id)
    user.update(password=make_password(newpassword))
    
    response = Response()
    response.data = {
        'message': 'Password changed successfully!'
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
@api_view(['PATCH'])
def UpdateUserInfo(request):
    valid_user_id = validateUser(request)
    response = Response()
    user = Customer.objects.get(id=valid_user_id)
    try:
        serializer = CustomerSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response.data = serializer.data
            response.status_code = status.HTTP_200_OK
        else:
            response.data=serializer.errors 
            response.status=status.HTTP_400_BAD_REQUEST
        return response
    except Exception as e:
        return Response(e)


# Update Profile - Get and Validate the jwt token from cookie then update specific user profilepic
@api_view(['PUT'])
def UpdateProfilePic(request):
    valid_user_id = validateUser(request)
    user = Customer.objects.filter(id=valid_user_id)
    olduser = user.first()
    path = 'media/' + str(olduser.profilePic)
    if os.path.isdir(path):
        shutil.rmtree(path) 

    user.update(profilePic=request.data['profilePic'])
    
    response = Response()
    response.data = {
        'message': 'Profile picture updated!'
    }
    return response