# app_spookies/serializers.py
from datetime import timedelta
from rest_framework import serializers
from .models import SpookyModel
from django.contrib.auth.models import User
from rest_framework.serializers import ListSerializer
from django.utils import timezone
from django.db import models
from rest_framework.exceptions import ValidationError

class UsernameRelatedField(serializers.ListField):  # Inherit from ListField
    """
    Custom field to validate usernames and convert them to User objects.
    """
    child = serializers.CharField()  # Specify the field type for each item

    def to_internal_value(self, data):
        users = []
        for username in data:
            try:
                from django.contrib.auth.models import User  # Assuming User model
                user = User.objects.get(username=username)
                users.append(user)
            except User.DoesNotExist:
                raise ValidationError('Invalid username: ' + username)
        return users


class SpookySerializer(serializers.ModelSerializer):
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
    class Meta:
        model = SpookyModel
        fields = ['id', 'sender', 'content', 'created_at', 'expiration_time']