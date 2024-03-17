# friendship/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('send-friend-request/', views.sendFriendRequestAPI, name='send friend request'),
    path('handle-friendship-request/', views.handleFriendshipRequestAPI, name='handle friend request'),
    path('remove-friend/', views.removeFriendAPI, name='remove friend'),
    path('my-friends/', views.friendsListAPI, name='list of my friends'),
]