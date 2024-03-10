# auth/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

from app_spookies.models import delete_expired_spookies
from .models import UserProfile


@api_view(['POST'])
@permission_classes([AllowAny])
def signupAPI(request):
    delete_expired_spookies()
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    phone_number = request.data.get('phone_number')

    if not (username and password and email and phone_number):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create UserProfile for the user
        profile = UserProfile.objects.create(user=user)
        profile.phone_number = phone_number
        profile.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'success',
            'data': {
                'token': token.key
            }
        }, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as e:
        return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def loginAPI(request):
    delete_expired_spookies()
    username_or_email_or_phone = request.data.get('username_or_email_or_phone')
    password = request.data.get('password')

    if not (username_or_email_or_phone and password):
        return Response({'error': 'Both username/email/phone and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = None
    if '@' in username_or_email_or_phone:  # Assume email
        user = authenticate(request, email=username_or_email_or_phone, password=password)
    elif username_or_email_or_phone.isdigit():  # Assume phone number
        profile = UserProfile.objects.filter(phone_number=username_or_email_or_phone).first()
        if profile:
            user = profile.user
            if not user.check_password(password):
                user = None
    else:
        user = authenticate(request, username=username_or_email_or_phone, password=password)

    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)
    return Response({
        'message': 'success',
        'data': {
            'token': token.key
        }
    }, status=status.HTTP_200_OK)