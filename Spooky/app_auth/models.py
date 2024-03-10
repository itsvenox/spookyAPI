# auth/models.py
from django.db import models
from django.contrib.auth.models import User, AbstractUser



# class User(AbstractUser):
#     email_verified = models.BooleanField(default=False)
#     verification_token = models.CharField(max_length=100, null=True, blank=True)

#     # Provide unique related_name arguments for groups and user_permissions fields
#     # to avoid clashes with the built-in User model
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='custom_user_set',  # Unique related_name
#         blank=True,
#         verbose_name='groups',
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='custom_user_set',  # Unique related_name
#         blank=True,
#         verbose_name='user permissions',
#         help_text='Specific permissions for this user.',
#         related_query_name='custom_user',
#     )



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15)
    profile_picture = models.URLField(blank=True, null=True)
    reputation = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username