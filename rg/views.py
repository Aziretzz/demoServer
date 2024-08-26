from datetime import timedelta

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Customer, JWTToken, GJWTToken
from .serializers import registrationCheck, UserSerializer, loginCheck, g_loginCheck, g_registrationCheck
from drf_spectacular.utils import extend_schema


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    tokens = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

    JWTToken.objects.create(
        user=user,
        access_token=tokens['access'],
        refresh_token=tokens['refresh'],
        access_expires_at=timezone.now() + timedelta(minutes=5),
        refresh_expires_at=timezone.now() + timedelta(days=1),
    )

    return tokens


def refresh_tokens(user):
    jwt_token = JWTToken.objects.get(user=user)
    refresh = RefreshToken.for_user(user)
    tokens = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    jwt_token.access_token = tokens['access']
    jwt_token.refresh_token = tokens['refresh']
    jwt_token.access_expires_at = timezone.now() + timedelta(minutes=5)
    jwt_token.refresh_expires_at = timezone.now() + timedelta(days=1)
    jwt_token.save()

    return tokens


@extend_schema(request=registrationCheck, responses={201: registrationCheck})
@api_view(['POST'])
@permission_classes([])
def r_register(request):
    serializer = registrationCheck(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens(user)
        return Response(tokens, status=201)
    return Response(serializer.errors, status=400)


@extend_schema(responses={200: UserSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_data(request):
    users = Customer.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@extend_schema(request=loginCheck, responses={200: loginCheck})
@api_view(['POST'])
def r_login(request):
    serializer = loginCheck(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        tokens = refresh_tokens(user)
        return Response({
            'refresh': tokens['refresh'],
            'access': tokens['access'],
            'message': 'Вход был удачным'
        }, status=200)
    return Response(serializer.errors, status=400)


@csrf_exempt
def rg(request):
    return HttpResponse("все работает")


def g_get_tokens(user):
    refresh = RefreshToken.for_user(user)
    tokens = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

    GJWTToken.objects.create(
        user=user,
        access_token=tokens['access'],
        refresh_token=tokens['refresh'],
        access_expires_at=timezone.now() + timedelta(minutes=5),
        refresh_expires_at=timezone.now() + timedelta(days=1),
    )

    return tokens


def g_refresh_tokens(user):
    jwt_token = GJWTToken.objects.get(user=user)
    refresh = RefreshToken.for_user(user)
    tokens = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    jwt_token.access_token = tokens['access']
    jwt_token.refresh_token = tokens['refresh']
    jwt_token.access_expires_at = timezone.now() + timedelta(minutes=5)
    jwt_token.refresh_expires_at = timezone.now() + timedelta(days=1)
    jwt_token.save()

    return tokens


@extend_schema(request=g_registrationCheck, responses={201: g_registrationCheck})
@api_view(['POST'])
def g_register(request):
    serializer = g_registrationCheck(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = g_get_tokens(user)
        return Response(tokens, status=201)
    return Response(serializer.errors, status=400)


@extend_schema(request=g_loginCheck, responses={200: g_loginCheck})
@api_view(['POST'])
def g_login(request):
    serializer = g_loginCheck(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        tokens = g_refresh_tokens(user)
        return Response({
            'refresh': tokens['refresh'],
            'access': tokens['access'],
            'message': 'Вход был удачным'
        }, status=200)
    return Response(serializer.errors, status=400)
