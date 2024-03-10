# friendship/models.py
from django.db import models
from django.contrib.auth.models import User
from app_auth.models import UserProfile


class FriendRequest(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_requests', on_delete=models.CASCADE)
    recipient = models.ForeignKey(UserProfile, related_name='received_requests', on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"From: {self.sender.user.username} - To: {self.recipient.user.username}"

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='user1_friendships', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2_friendships', on_delete=models.CASCADE)
    started_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.username} - {self.user2.username}"