# spookies/views.py
from datetime import timedelta
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import SpookyModel
from .serializers import ReceivedSpookySerializer, SpookySerializer
from django.utils import timezone


from django.contrib.auth.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_spooky(request):
    try:
        sender = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        return Response({"message": "Invalid sender ID."}, status=status.HTTP_400_BAD_REQUEST)

    request.data.update({'sender': sender.id})
    request.data.update({'expiration_time': timezone.now() + timedelta(minutes=3)})
    
    serializer = SpookySerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        # Extract friend usernames from request data
        friend_usernames = request.data.get('friends', [])
        
        # Validate friend usernames and check if they are friends
        friends = []
        for username in friend_usernames:
            try:
                friend = User.objects.get(username=username)
                if friend in sender.friends.all():  # Assuming there's a ManyToManyField called 'friends' on the User model
                    friends.append(friend)
                else:
                    return Response({"message": f"{username} is not a friend of the current user."}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"message": f"User '{username}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        # If at least one valid friend exists, handle spookies for existing friends
        if friends:
            # Check if any previous spookies exist for the sender and current friend(s)
            existing_spookies = SpookyModel.objects.filter(sender=sender, friends__in=friends, expiration_time__gt=timezone.now())
            for spooky in existing_spookies:
                # Remove the current friend(s) from the previous spookies' recipients
                spooky.friends.remove(*friends)
                spooky.save()

            serializer.validated_data['friends'] = friends
            spooky = serializer.save()

            # Retrieve the latest spookies for each friend after updating
            latest_spookies = {}
            for friend in friends:
                latest_spooky = SpookyModel.objects.filter(sender=sender, friends=friend, expiration_time__gt=timezone.now()).order_by('-created_at').first()
                if latest_spooky:
                    latest_spookies[friend.username] = latest_spooky.id
            
            serialized_spooky = SpookySerializer(instance=spooky)
            response_data = {
                "spooky": serialized_spooky.data,
                "latest_spookies": latest_spookies
            }
            return JsonResponse(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "No valid friends provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_spookies(request):
    user = request.user
    spookies_sent = SpookyModel.objects.filter(sender=user)
    spookies_received = SpookyModel.objects.filter(friends=user)

    # Serialize received spookies with specific fields
    serializer_received = ReceivedSpookySerializer(spookies_received, many=True)

    return Response(
        {
            'sent_spookies': SpookySerializer(spookies_sent, many=True).data,
            'received_spookies': serializer_received.data
        }, status=status.HTTP_200_OK
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_spooky(request, spooky_id):
    try:
        spooky = SpookyModel.objects.get(pk=spooky_id)
    except SpookyModel.DoesNotExist:
        return Response({"message": "Spooky message does not exist."}, status=status.HTTP_404_NOT_FOUND)

    # Check if the authenticated user is the sender of the spooky message
    if spooky.sender != request.user:
        return Response({"message": "You are not authorized to delete this spooky message."}, status=status.HTTP_403_FORBIDDEN)

    spooky.delete()
    return Response({"message": "Spooky message deleted successfully."}, status=status.HTTP_204_NO_CONTENT)