from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from api.models.cloth import Cloth
from api.models.serializers import ClothSerializer
from api.common import validateUser
import jwt
import datetime
import os
import shutil

# get all items 
@api_view(['GET'])
def getItems(request):
    valid_user_id = validateUser(request)
    if valid_user_id:
        items = Cloth.objects.all()
        serializer = ClothSerializer(instance=items, many=True)
        return Response(serializer.data)

# create new Cloth
@api_view(['POST'])
def addItem(request):
    valid_user_id = validateUser(request)
    pre_save = {
        "name": request.data["name"],
        "description": request.data["description"]
    }
    serializer = ClothSerializer(data=pre_save)
    if serializer.is_valid():
        serializer.save()
        data = Cloth.objects.get(id=serializer.data["id"])
        serializer = ClothSerializer(instance=data, data=request.data)
        if serializer.is_valid():
            serializer.save()
    return Response(serializer.data)


# get/update/delete single Cloth
@api_view(['GET', 'PUT', 'POST', 'DELETE'])
def singleItem(request, pk):
    valid_user_id = validateUser(request)
    if valid_user_id:
        if request.method == "GET":
            hasError = False
            try:
                instance = Cloth.objects.get(id=pk)
            except ObjectDoesNotExist:
                error = {"error": "Cloth is not found!"}
                hasError = True

            if not hasError:
                serializer = ClothSerializer(instance=instance, many=False)
                return Response(serializer.data)
            return Response(error, request)

        elif request.method == "PUT":
            hasError = False
            try:
                if 'icon' in request.data:
                    olduser = Cloth.objects.filter(id=pk).first()
                    os.remove('media/' + str(olduser.icon))
                data = Cloth.objects.get(id=pk)
                serializer = ClothSerializer(
                    instance=data, data=request.data)
            except ObjectDoesNotExist:
                error = {"error": "Cloth is not found!"}
                hasError = True

            if not hasError and serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(error)

        elif request.method == "DELETE":
            data = Cloth.objects.get(id=pk)
            path = 'media/cloth/' + str(pk)
            if os.path.isdir(path):
                shutil.rmtree(path) 
            data.delete()
            return Response({"response": 'Cloth deleted successfully'})
