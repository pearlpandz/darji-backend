from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from api.models.order import Order
from api.models.cloth import Cloth
from api.models.serializers import OrderSerializer, ClothSerializer

def index(request):
    items = Order.objects.all()
    serializer = OrderSerializer(instance=items, many=True)
    print(len(serializer.data))
    return render(request, 'orders/list.html', { "orders": serializer.data })

def ViewOrder(request, pk):
    error = None
    reseponse = None
    try:
        items = Order.objects.get(id=pk)
        orderSerializer = OrderSerializer(instance=items, many=False)
        
        cloth_id = orderSerializer.data['cloth_id']
        clothInstance = Cloth.objects.get(id=cloth_id)
        clothSerializer = ClothSerializer(instance=clothInstance, many=False)
        
        reseponse = orderSerializer.data
        reseponse['cloth'] = clothSerializer.data
    except ObjectDoesNotExist:
        error = {"error": "Cloth is not found!"}
    print(reseponse)
    return render(request, 'orders/detail.html', {"order": reseponse, "error": error})   
    