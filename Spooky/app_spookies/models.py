# app_spookies/models.py
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver



class SpookyModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_spookies')
    friends = models.ManyToManyField(User, related_name='received_spookies')  # Use ManyToManyField
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField()

    @classmethod
    def create_spooky(cls, sender, content, friends):
        now = timezone.now()
        expiration_time = now + timedelta(minutes=3)  # Set expiration time to 1 hour from now

        spooky = cls.objects.create(
            sender=sender,
            content=content,
            created_at=now,
            expiration_time=expiration_time,
        )
        spooky.friends.set(friends)  # Set friends using User objects directly
        return spooky


    def is_expired(self):
        return self.expiration_time < timezone.now()


def delete_expired_spookies():
    expired_spookies = SpookyModel.objects.filter(expiration_time__lt=timezone.now())
    expired_spookies.delete()
