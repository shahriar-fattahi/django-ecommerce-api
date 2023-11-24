from django.conf import settings
from rest_framework import authentication, exceptions
import jwt
from . import models


class CustomUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms="HS256")
        except:
            raise exceptions.AuthenticationFailed("Unauthorized")

        try:
            user = models.User.objects.get(id=payload["id"])
        except models.User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid authorize key")

        return (user, None)
