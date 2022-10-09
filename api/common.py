from rest_framework.exceptions import AuthenticationFailed
import jwt

def validateUser(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Token Missing!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed({"message": 'Token Expired, Unauthenticated!'})

    return payload['id']

