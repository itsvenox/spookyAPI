# friendship/views.py
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from app_spookies.models import delete_expired_spookies
from .models import FriendRequest, Friendship
from django.db import models 
from utils import calculate_duration
from datetime import timedelta


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendFriendRequestAPI(request):
    delete_expired_spookies()
    sender_profile = request.user.profile

    try:
        recipient_username = request.data['recipient']
        recipient_user = User.objects.get(username=recipient_username)
        recipient_profile = recipient_user.profile

        # Check if the friendship already exists
        if Friendship.objects.filter(user1=sender_profile.user, user2=recipient_user) or Friendship.objects.filter(user1=recipient_user, user2=sender_profile.user):
            return Response({'message': 'Friendship already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the friend request already exists
        friend_request = FriendRequest.objects.filter(sender=sender_profile, recipient=recipient_profile).first()
        if friend_request:
            friend_request.delete()

        friend_request = FriendRequest(sender=sender_profile, recipient=recipient_profile)
        friend_request.save()

        return Response({'message': 'Friend request sent successfully'}, status=status.HTTP_201_CREATED)

    except User.DoesNotExist:
        return Response({'message': 'Recipient user does not exist'}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handleFriendshipRequestAPI(request):
    delete_expired_spookies()
    recipient_profile = request.user.profile

    try:
        sender_username = request.data['sender']
        sender_user = User.objects.get(username=sender_username)
        sender_profile = sender_user.profile

        # Check if the friend request exists
        friend_request = FriendRequest.objects.get(sender=sender_profile, recipient=recipient_profile, accepted=False)

        action = request.data.get('action')  # Check if the action is provided (accept or reject)
        if action == 'accept':
            # Accept the friend request and create friendship
            friend_request.accepted = True
            friend_request.save()

            friendship = Friendship(user1=sender_user, user2=request.user)
            friendship.save()

            # Delete the friend request after accepting
            friend_request.delete()

            return Response({'message': 'Friend request accepted and friendship created'}, status=status.HTTP_201_CREATED)
        elif action == 'reject':
            # Delete the friend request
            friend_request.delete()
            return Response({'message': 'Friend request rejected'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({'error': 'Sender user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Friend request does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def removeFriendAPI(request):
    user_profile = request.user.profile

    try:
        friend_username = request.data['friend']
        friend_user = User.objects.get(username=friend_username)
        friend_profile = friend_user.profile

        # Check if a friendship exists between the current user and the friend
        friendship = Friendship.objects.filter(
            (models.Q(user1=user_profile.user) & models.Q(user2=friend_user)) | 
            (models.Q(user1=friend_user) & models.Q(user2=user_profile.user))
        ).first()

        if friendship:
            # Delete the friendship
            friendship.delete()
            return Response({'message': 'Friend removed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Friendship does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({'error': 'Friend user does not exist'}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friendsListAPI(request):
    user_profile = request.user.profile

    # Retrieve all friendships where the current user is involved
    friendships = Friendship.objects.filter(
        models.Q(user1=user_profile.user) | models.Q(user2=user_profile.user)
    )

    friends = []
    for friendship in friendships:
        # Determine the friend based on the current user's profile
        friend = friendship.user1 if friendship.user2 == user_profile.user else friendship.user2

        friends.append({
            'id': friend.id,
            'username': friend.username,
            'profile_picture': friend.profile.profile_picture,
            'friends_since': calculate_duration.calculate(friendship.started_date)
        })

    return Response({'friends': friends}, status=status.HTTP_200_OK)
