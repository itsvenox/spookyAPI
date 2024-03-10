from django.test import TestCase

# Create your tests here.





# # app_spookies/models.py
# from datetime import timedelta
# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.utils import timezone
# from django.dispatch import receiver



# class SpookyModel(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_spookies')
#     friends = models.ManyToManyField(User, related_name='received_spookies')  # Use ManyToManyField
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     expiration_time = models.DateTimeField()

#     @classmethod
#     def create_spooky(cls, sender, content, friends):
#         now = timezone.now()
#         expiration_time = now + timedelta(minutes=1)  # Set expiration time to 1 hour from now

#         spooky = cls.objects.create(
#             sender=sender,
#             content=content,
#             created_at=now,
#             expiration_time=expiration_time,
#         )
#         spooky.friends.set(friends)  # Set friends using User objects directly
#         return spooky



# # spookies/views.py
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_spooky(request):
#     try:
#         sender = User.objects.get(pk=request.user.id)
#     except User.DoesNotExist:
#         return Response({"message": "Invalid sender ID."}, status=status.HTTP_400_BAD_REQUEST)

#     request.data.update({'sender': sender.id})
#     request.data.update({'expiration_time': timezone.now() + timedelta(minutes=1)})
    
#     serializer = SpookySerializer(data=request.data, context={'request': request})
    
#     if serializer.is_valid():
#         # Extract friend usernames from request data
#         friend_usernames = request.data.get('friends', [])
        
#         # Validate friend usernames
#         friends = []
#         for username in friend_usernames:
#             try:
#                 friend = User.objects.get(username=username)
#                 friends.append(friend)
#             except User.DoesNotExist:
#                 return Response({"message": f"User '{username}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # If at least one valid friend exists, update spookies for existing friends
#         if friends:
#             existing_spookies = SpookyModel.objects.filter(sender=sender, expiration_time__gt=timezone.now())
#             for spooky in existing_spookies:
#                 spooky.friends.add(*friends)
#                 spooky.save()
            
#             serializer.validated_data['friends'] = friends
#             spooky = serializer.save()
#             serialized_spooky = SpookySerializer(instance=spooky)
#             return Response(serialized_spooky.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"message": "No valid friends provided."}, status=status.HTTP_400_BAD_REQUEST)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# when the same user send a spookie to the same friend again, it will be deleted from the table app_spookies_spookymodel_friends
# for example in this image the user 4 has got three spookies from the same user1  and they are all visible to him.
# i want just the last one to be visible to him.



# # app_spookies/models.py
# from datetime import timedelta
# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.utils import timezone
# from django.dispatch import receiver



# class SpookyModel(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_spookies')
#     friends = models.ManyToManyField(User, related_name='received_spookies')  # Use ManyToManyField
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     expiration_time = models.DateTimeField()

#     @classmethod
#     def create_spooky(cls, sender, content, friends):
#         now = timezone.now()
#         expiration_time = now + timedelta(minutes=1)  # Set expiration time to 1 hour from now

#         spooky = cls.objects.create(
#             sender=sender,
#             content=content,
#             created_at=now,
#             expiration_time=expiration_time,
#         )
#         spooky.friends.set(friends)  # Set friends using User objects directly
#         return spooky


#     @classmethod
#     def remove_expired_spookies(cls):
#         now = timezone.now()
#         expired_spookies = cls.objects.filter(expiration_time__lt=now)
#         expired_spookies.delete()


# @receiver(post_save, sender=SpookyModel)
# def remove_expired_spookies(sender, instance, **kwargs):
#     SpookyModel.remove_expired_spookies()

# # app_spookies/serializers.py
# from datetime import timedelta
# from rest_framework import serializers
# from .models import SpookyModel
# from django.contrib.auth.models import User
# from rest_framework.serializers import ListSerializer
# from django.utils import timezone
# from django.db import models
# from rest_framework.exceptions import ValidationError

# class UsernameRelatedField(serializers.ListField):  # Inherit from ListField
#     """
#     Custom field to validate usernames and convert them to User objects.
#     """
#     child = serializers.CharField()  # Specify the field type for each item

#     def to_internal_value(self, data):
#         users = []
#         for username in data:
#             try:
#                 from django.contrib.auth.models import User  # Assuming User model
#                 user = User.objects.get(username=username)
#                 users.append(user)
#             except User.DoesNotExist:
#                 raise ValidationError('Invalid username: ' + username)
#         return users


# class SpookySerializer(serializers.ModelSerializer):
#     friends = serializers.SlugRelatedField(
#         slug_field='username',
#         queryset=User.objects.all(),
#         many=True,
#         required=False
#     )

#     class Meta:
#         model = SpookyModel
#         fields = ('id', 'sender', 'content', 'expiration_time', 'friends')


# class ReceivedSpookySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SpookyModel
#         fields = ['id', 'content', 'created_at', 'expiration_time']




# # spookies/views.py
# from datetime import timedelta
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from .models import SpookyModel
# from .serializers import ReceivedSpookySerializer, SpookySerializer
# from django.utils import timezone


# from django.contrib.auth.models import User


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_spooky(request):
#     try:
#         sender = User.objects.get(pk=request.user.id)
#     except User.DoesNotExist:
#         return Response({"message": "Invalid sender ID."}, status=status.HTTP_400_BAD_REQUEST)

#     request.data.update({'sender': sender.id})
#     request.data.update({'expiration_time': timezone.now() + timedelta(minutes=1)})
    
#     serializer = SpookySerializer(data=request.data, context={'request': request})
    
#     if serializer.is_valid():
#         # Extract friend usernames from request data
#         friend_usernames = request.data.get('friends', [])
        
#         # Validate friend usernames
#         friends = []
#         for username in friend_usernames:
#             try:
#                 friend = User.objects.get(username=username)
#                 friends.append(friend)
#             except User.DoesNotExist:
#                 return Response({"message": f"User '{username}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # If at least one valid friend exists, save the spookie
#         if friends:
#             serializer.validated_data['friends'] = friends
#             spooky = serializer.save()
#             serialized_spooky = SpookySerializer(instance=spooky)
#             return Response(serialized_spooky.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"message": "No valid friends provided."}, status=status.HTTP_400_BAD_REQUEST)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# if i am user1 and i have send a spooky "hi user3 and user4" to my friends user3 and user4. and in less then 1 minute i have send another spooky to user4 "hi user 4". if that happend i want the server to delete the previos spooky i send to him from him. and send him the new one from me
