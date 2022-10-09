from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
from api.models.category import Category
from api.models.serializers import CategorySerializer
from api.common import validateUser
import jwt
import datetime
import os
import shutil

# get all companies 
@api_view(['GET'])
def getCategories(request):
    valid_user_id = validateUser(request)
    if valid_user_id:
        companies = Category.objects.all()
        serializer = CategorySerializer(instance=companies, many=True)
        return Response(serializer.data)

# create new Category
@api_view(['POST'])
def addGlobalCategory(request):
    valid_user_id = validateUser(request)
    pre_save = {
        "name": request.data["name"],
        "description": request.data["description"]
    }
    serializer = CategorySerializer(data=pre_save)
    if serializer.is_valid():
        serializer.save()
        data = Category.objects.get(id=serializer.data["id"])
        serializer = CategorySerializer(instance=data, data=request.data)
        if serializer.is_valid():
            serializer.save()
    return Response(serializer.data)


# get/update/delete single Category
@api_view(['GET', 'PUT', 'POST', 'DELETE'])
def globalCategoryView(request, pk):
    valid_user_id = validateUser(request)
    if valid_user_id:
        if request.method == "GET":
            hasError = False
            try:
                instance = Category.objects.get(id=pk)
            except ObjectDoesNotExist:
                error = {"error": "Category is not found!"}
                hasError = True

            if not hasError:
                serializer = CategorySerializer(instance=instance, many=False)
                return Response(serializer.data)
            return Response(error, request)

        elif request.method == "PUT":
            hasError = False
            try:
                if 'icon' in request.data:
                    olduser = Category.objects.filter(id=pk).first()
                    os.remove('media/' + str(olduser.icon))
                data = Category.objects.get(id=pk)
                serializer = CategorySerializer(
                    instance=data, data=request.data)
            except ObjectDoesNotExist:
                error = {"error": "Category is not found!"}
                hasError = True

            if not hasError and serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(error)

        elif request.method == "DELETE":
            data = Category.objects.get(id=pk)
            path = 'media/category/' + str(pk)
            if os.path.isdir(path):
                shutil.rmtree(path) 
            data.delete()
            return Response({"response": 'Category deleted successfully'})
