from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from api.models.property import Property, PropertyImage, PropertyVideo
from api.models.customer import Customer
from api.models.category import Category
from api.models.serializers import PropertySerializer, CustomerSerializer, CategorySerializer, PropertyImageSerializer, PropertyVideoSerializer
from api.common import validateUser
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import jwt
import datetime
import json

# Property API
# create new product


@api_view(['POST'])
def add_product(request):
    serializer = PropertySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# get all products
@api_view(['GET'])
def getProperties(request):
    valid_user_id = validateUser(request)
    if valid_user_id:
        instances = Property.objects.all()
        properties = []
        for instance in instances:
            hasError = False
            try:
                img_instance = PropertyImage.objects.filter(product=instance.id)
                video_instance = PropertyVideo.objects.filter(product=instance.id)

            except ObjectDoesNotExist:
                products = {"error": "Property is not found!"}
                hasError = True

            if not hasError:
                propertyItem = {
                    "id": instance.id,
                    "name": instance.name,
                    "description": instance.description,
                    "ratings": instance.ratings,
                    "price": instance.price,
                    "noOfBed": instance.noOfBed,
                    "noOfBathroom": instance.noOfBathroom,
                    "sqft": instance.sqft,
                    "location": instance.location,
                    "category": [{
                        "id": category.id,
                        "name": category.name,
                        "description": category.description,
                        "icon": str(category.icon)
                    } for category in instance.category.all()],
                    "propertyType": [{
                        "id": propertyType.id,
                        "name": propertyType.name,
                        "description": propertyType.description,
                    } for propertyType in instance.propertyType.all()],
                    "images": [str(url) for url in img_instance.all()],
                    "videos": [str(url) for url in video_instance.all()],
                }
                properties.append(propertyItem)
        return Response(properties)


# get/update/delete single product
@api_view(['GET', 'PATCH', 'DELETE'])
def PropertyView(request, pk):
    valid_user_id = validateUser(request)
    if valid_user_id:
        if request.method == "GET":
            hasError = False
            try:
                instance = Property.objects.get(id=pk)
                img_instance = PropertyImage.objects.filter(product=pk)
                video_instance = PropertyVideo.objects.filter(product=pk)

            except ObjectDoesNotExist:
                products = {"error": "Property is not found!"}
                hasError = True

            if not hasError:
                return Response({
                    "id": instance.id,
                    "name": instance.name,
                    "description": instance.description,
                    "ratings": instance.ratings,
                    "price": instance.price,
                    "noOfBed": instance.noOfBed,
                    "noOfBathroom": instance.noOfBathroom,
                    "sqft": instance.sqft,
                    "location": instance.location,
                    "category": [{
                        "id": category.id,
                        "name": category.name,
                        "description": category.description,
                        "icon": str(category.icon)
                    } for category in instance.category.all()],
                    "propertyType": [{
                        "id": propertyType.id,
                        "name": propertyType.name,
                        "description": propertyType.description,
                    } for propertyType in instance.propertyType.all()],
                    "images": [str(url) for url in img_instance.all()],
                    "videos": [str(url) for url in video_instance.all()],
                })
            return Response(products, request)

        elif request.method == "PATCH":
            hasError = False
            try:
                product = Property.objects.get(id=pk)
                serializer = PropertySerializer(
                    instance=product, data=request.data)
            except ObjectDoesNotExist:
                products = {"error": "Property is not found!"}
                hasError = True

            if not hasError and serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(products)

        elif request.method == "DELETE":
            product = Property.objects.get(id=pk)
            product.delete()
            return Response('Property deleted successfully')
