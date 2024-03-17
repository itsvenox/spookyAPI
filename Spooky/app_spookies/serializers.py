# app_spookies/serializers.py
from datetime import timedelta
from rest_framework import serializers

from app_auth.models import UserProfile
from .models import SpookyModel
from django.contrib.auth.models import User
from rest_framework.serializers import ListSerializer
from django.utils import timezone
from django.db import models
from rest_framework.exceptions import ValidationError



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)

class SenderSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, obj):
        try:
            user_profile = UserProfile.objects.get(user=obj)
            return user_profile.profile_picture
        except UserProfile.DoesNotExist:
            return None

    class Meta:
        model = User
        fields = ('id', 'username', 'profile_picture')


class SpookyListSerializer(serializers.ModelSerializer):
    sender = SenderSerializer()
    friends = serializers.SerializerMethodField()
    def get_friends(self, obj):
        return [friend.username for friend in obj.friends.all()]

    class Meta:
        model = SpookyModel
        fields = ('id', 'sender', 'content', 'created_at', 'expiration_time', 'friends')



class SpookyCreateSerializer(serializers.ModelSerializer):
    friends = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = SpookyModel
        fields = ('id', 'sender', 'content', 'created_at', 'expiration_time', 'friends')




class ReceivedSpookySerializer(serializers.ModelSerializer):
    sender = SenderSerializer()

    class Meta:
        model = SpookyModel
        fields = ('id', 'content', 'expiration_time', 'created_at', 'sender')
