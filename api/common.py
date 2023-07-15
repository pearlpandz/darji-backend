from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings

def validateUser(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Token Missing!')

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed({"message": 'Token Expired, Unauthenticated!'})
    print(payload)
    return payload['user_id']