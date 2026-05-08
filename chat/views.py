from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics,permissions
from chat.serializer import roomSerializer
from chat.models import Room,Messages
from django.contrib.auth.decorators import login_required
from account.models import User

class roomCreate(generics.CreateAPIView):
    room=Room.objects.all()
    serializer_class=roomSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        room_name=self.kwargs.get('room_name')
        print(room_name)
        serializer.save(room_name=room_name,created_by=self.request.user)


@login_required
def roomAll(request):
    room=Room.objects.select_related('created_by').all()
    # users=User.objects.filter(is_staff=True)
    return render(request,'chat/roomsAll.html',{
        'room':room,
    })




@login_required
def room(request,room_name):
    room=Room.objects.get(room_name=room_name)
    messages=Messages.objects.filter(room_id=room.id).select_related('created_by')
    if request.user.is_staff:
        if room.status==room.WAITING:
            room.status=room.ACTIVE
            room.save()
    return render(request,'chat/partials/small_chat_room.html',{
        'room':room,
        'messages': messages

    })
