from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from api.common import validateUser
from api.models.order import Order, ReferenceImage
from api.models.serializers import OrderSerializer, ReferenceImageSerializer

# create new order with reference image and measurements
@api_view(['GET'])
def getOrderList(request):
    valid_user_id = validateUser(request)
    if valid_user_id:
        items = Order.objects.all()
        serializer = OrderSerializer(instance=items, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def getSingleOrder(request, pk):
    valid_user_id = validateUser(request)
    if valid_user_id:
        hasError = False
        try:
            items = Order.objects.get(id=pk)
        except ObjectDoesNotExist:
            error = {"error": "Cloth is not found!"}
            hasError = True
        if not hasError:
            serializer = OrderSerializer(instance=items, many=False)
            return Response(serializer.data)
        return Response(error, request)

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

@api_view(['POST'])
def orderReferenceImage(request, pk):
    valid_user_id = validateUser(request)
    hasError = False
    try:
        res = []
        references = dict((request.FILES).lists()).get('reference', None)
        print(len(references))
        if references:
            for reference in references:
                obj = {
                    "orderId": pk,
                    "url": reference
                }
                serializer = ReferenceImageSerializer(data=obj)
                if serializer.is_valid():
                    serializer.save()
                    res.append(serializer.data)
    except:
        error = {"error": "Something went wrong"}
        hasError = True
    
    if not hasError:
        return Response(res)
    return Response(error)