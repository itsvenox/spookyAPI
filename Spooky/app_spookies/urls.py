from django.urls import path

from . import views

urlpatterns = [
    path('create-blobie/', views.create_spooky, name='create_blobie'),
    path('list-blobies/', views.list_spookies, name='delete_blobie'),
    path('delete-spooky/<int:spooky_id>/', views.delete_spooky, name='delete_spooky'),
]