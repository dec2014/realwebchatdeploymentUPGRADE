from django.urls import path
from . import views


urlpatterns=[
    path('create-room/<str:room_name>/',views.roomCreate.as_view(),name='room-create'),
    path('rooms/',views.roomAll,name='rooms'),
    path('chat-admin/<str:room_name>/',views.room,name='room'),
]
