from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from api.models.property import Property
from api.models.customer import Customer
from api.models.category import Category
from api.models.serializers import PropertySerializer, CustomerSerializer, CategorySerializer
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
        instance = Property.objects.all()

        serializer = PropertySerializer(instance=instance, many=True)
        return Response(serializer.data)


# get/update/delete single product
@api_view(['GET', 'PATCH', 'DELETE'])
def PropertyView(request, pk):
    valid_user_id = validateUser(request)
    if valid_user_id:
        if request.method == "GET":
            hasError = False
            try:
                instance = Property.objects.get(id=pk)
                # and then for fetch the author
                # for category in instance.category.all():
                #     print(category)

            except ObjectDoesNotExist:
                products = {"error": "Property is not found!"}
                hasError = True

            if not hasError:
                serializer = PropertySerializer(instance=instance, many=False)
                return Response({
                    "name": serializer.data['name'], 
                    "description": serializer.data['description'], 
                    "category": [{
                        "id": category.id,
                        "name": category.name, 
                        "description": category.description,
                        "icon": str(category.icon) 
                        } for category in instance.category.all()]
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
