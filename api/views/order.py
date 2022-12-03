from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from api.common import validateUser
from api.models.order import Order
from api.models.serializers import OrderSerializer

# create new order with reference image and measurements


@api_view(['POST'])
def newOrder(request):
    valid_user_id = validateUser(request)
    request.data['userId'] = valid_user_id
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# get/update/delete single Cloth
@api_view(['PUT'])
def updateOrder(request, pk):
    valid_user_id = validateUser(request)
    hasError = False
    try:
        data = Order.objects.get(id=pk)
        serializer = OrderSerializer(
            instance=data, data=request.data)
    except ObjectDoesNotExist:
        error = {"error": "Cloth is not found!"}
        hasError = True

    if not hasError and serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(error)


# get/update/delete single Cloth
# @api_view(['PUT'])
# def clothSelection(request, pk):
