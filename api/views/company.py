from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from api.models.company import Company
from api.models.serializers import CompanySerializer
from api.common import validateUser
from django.core.exceptions import ObjectDoesNotExist
import jwt, datetime
import os
import shutil

#get all companies
@api_view(['GET'])
def get_companies(request):  
    companies = Company.objects.all()
    serializer = CompanySerializer(instance=companies, many=True)
    return Response(serializer.data)
        
# create new company
@api_view(['POST'])
def addCompany(request):
    pre_save = {
        "name": request.data["name"],
        "description": request.data["description"]
    }
    serializer = CompanySerializer(data=pre_save)
    if serializer.is_valid():
        serializer.save()
        data = Company.objects.get(id=serializer.data["id"])    
        serializer = CompanySerializer(instance=data, data=request.data)
        if serializer.is_valid():
            serializer.save()
    return Response(serializer.data)


#get/update/delete single company
@api_view(['GET','PUT','POST','DELETE'])
def CompanyView(request,pk): 
    valid_user_id = validateUser(request)
    if valid_user_id:
        if request.method == "GET":
            hasError = False
            try:
                instance = Company.objects.get(id=pk)
            except ObjectDoesNotExist:
                error = {"error": "Company is not found!"}
                hasError = True

            if not hasError:    
                serializer = CompanySerializer(instance=instance, many=False)
                return Response(serializer.data)
            return Response(error, request);

        elif request.method == "PUT":
            hasError = False
            try:
                if 'logo' in request.data:
                    olduser = Company.objects.filter(id=pk).first()
                    os.remove('media/' + str(olduser.logo))
                if 'banner' in request.data:
                    olduser = Company.objects.filter(id=pk).first()
                    os.remove('media/' + str(olduser.banner))
                data = Company.objects.get(id=pk)    
                serializer = CompanySerializer(instance=data, data=request.data)
            except ObjectDoesNotExist:
                error = {"error": "Company is not found!"}
                hasError = True
                
            if not hasError and serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(error)

        elif request.method == "DELETE":
            data = Company.objects.get(id=pk)   
            path = 'media/company/' + str(pk)
            if os.path.isdir(path):
                shutil.rmtree(path) 
            data.delete()
            return Response({"response": 'Company deleted successfully'})
