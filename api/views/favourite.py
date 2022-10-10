from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from api.common import validateUser

from api.models.serializers import FavouritePropertySerializer
from api.models.property import FavouriteProperty

@api_view(['POST'])
def addToFavourite(request):
    valid_user_id = validateUser(request)
    if valid_user_id:
        data = {
            "property": request.data["property"],
            "customer": valid_user_id
        }
        serializer = FavouritePropertySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    else:
        AuthenticationFailed('Unauthorized!')

@api_view(['DELETE'])
def RemovePropertyFromFavourites(request, pk):
    valid_user_id = validateUser(request)
    if valid_user_id:
        instance = FavouriteProperty.objects.get(id=pk)
        instance.delete()
        return Response('Property removed from your favourites successfully')
    else:
        AuthenticationFailed('Unauthorized!')

# get all products
@api_view(['GET'])
def getAllFavourites(request):
    valid_user_id = validateUser(request)
    if valid_user_id:
        instance = FavouriteProperty.objects.filter(customer=valid_user_id)
        serializer = FavouritePropertySerializer(instance=instance, many=True)
        return Response(serializer.data)
    else:
        AuthenticationFailed('Unauthorized!')