from django.conf import settings


import jwt
from rest_framework import generics, permissions, serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name="", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


# TOKENS


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        user_info = {}

        user_info["id"] = str(self.user.id)
        user_info["email"] = str(self.user.email)
        if self.user.full_name is None:
            user_info["name"] = str(self.user.username)
        else:
            user_info["name"] = str(self.user.full_name)
        user_info["role"] = "TENANT_ADMIN"

        data[
            "userInfo"
        ] = user_info  # jwt.encode(user_info,settings.SIGNING_KEY,algorithm=('HS512'))

        decoded = jwt.decode(
            str(refresh.access_token),
            settings.SIGNING_KEY,
            algorithms=["HS512"],
            audience="api.caterchain",
        )
        data["expiresAt"] = decoded["exp"]

        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = RefreshToken(attrs["refresh"])

        data["access"] = str(refresh.access_token)

        decoded = jwt.decode(
            str(refresh.access_token),
            settings.SIGNING_KEY,
            algorithms=["HS512"],
            audience="api.caterchain",
        )
        data["expiresAt"] = decoded["exp"]

        return data
