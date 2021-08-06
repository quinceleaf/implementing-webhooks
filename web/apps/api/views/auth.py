from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.middleware import csrf
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST


import datetime as dt
from decimal import Decimal
import json
import re


import jwt
from rest_framework import serializers, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from apps.api import serializers as api_serializers


""" 
Naming convention: <Entity><Action>Api
"""


# TOKEN VIEWS


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializers.CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = api_serializers.CustomTokenRefreshSerializer


# API VIEWS


def get_csrf(request):
    response = JsonResponse({"detail": "CSRF cookie set"})
    response["X-CSRFToken"] = get_token(request)
    return response


def get_tokens_for_user(user):

    # User info
    user_info = {}

    user_info["id"] = str(user.id)
    user_info["email"] = str(user.email)
    if user.full_name is None:
        user_info["name"] = str(user.username)
    else:
        user_info["name"] = str(user.full_name)
    user_info["role"] = "TENANT_ADMIN"

    # Refresh & access token
    refresh = RefreshToken.for_user(user)

    # Token expiration value
    decoded = jwt.decode(
        str(refresh.access_token),
        settings.SIGNING_KEY,
        algorithms=["HS512"],
        audience="api.caterchain",
    )
    expires_at = decoded["exp"]

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "userInfo": user_info,
        "expiresAt": expires_at,
    }


def get_data_for_user(user):
    user_info = {}

    user_info["id"] = str(user.id)
    user_info["email"] = str(user.email)
    if user.full_name is None:
        user_info["name"] = str(user.username)
    else:
        user_info["name"] = str(user.full_name)
    user_info["role"] = "TENANT_ADMIN"  # Default TODO: lookup user roles during login

    return {
        "userInfo": user_info,
    }


@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return JsonResponse(
            {"detail": "Please provide username and password."}, status=400
        )

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({"detail": "Invalid credentials."}, status=400)

    login(request, user)
    return JsonResponse({"detail": "Successfully logged in."})


def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "You're not logged in."}, status=400)

    logout(request)
    return JsonResponse({"detail": "Successfully logged out."})
