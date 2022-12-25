from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from api.models.pincode import Pincode
from api.models.serializers import PinSerializer
from api.common import validateUser
import jwt
import datetime
import os
import shutil


@api_view(['GET'])
def get_pincodes(request):
    valid_user_id = validateUser(request)
    if valid_user_id:
        items = Pincode.objects.all()
        serializer = PinSerializer(instance=items, many=True)
        return Response(serializer.data)
