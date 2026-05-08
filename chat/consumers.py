import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .templatetags.chatextras import initials
from django.utils.timesince import timesince
from .models import Room,Messages
from account.models import User
import asyncio

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_name_group=f'chat_{self.room_name}'
        # await asyncio.sleep(0.1)
        # await self.get_room()
        await self.channel_layer.group_add(self.room_name_group,self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        print(self.scope['user'])
        await self.channel_layer.group_discard(self.room_name_group,self.channel_name)

    async def receive(self, text_data = None, bytes_data = None):

        text_data_json=json.loads(text_data)
        type=text_data_json['type']
        message=text_data_json['body']
        created_by=self.scope['user']
        created_by_name=self.scope['user'].name
        created_by_id=str(self.scope['user'].id)
        room=text_data_json.get('room')

        print('type',created_by_name)

        if type=='message':
            nw_message= await self.create_messages(created_by,room,message)
            # print(nw_message)
            await self.channel_layer.group_send(
                self.room_name_group,{
                    'type':'chat_message',
                    'message':message,
                    'created_by_name':created_by_name,
                    'created_by_id':created_by_id,
                    'room':room,
                    'initials':initials(created_by_name),
                    'created_at':timesince(nw_message.created_at)

                }
            )
    async def chat_message(self,event):
        await self.send(text_data=json.dumps(event))
        


    

    @sync_to_async
    def create_messages(self,created_by,room,message):
        room1=Room.objects.get(room_name=room)
        message=Messages.objects.create(body=message, created_by=created_by,room=room1)
        
        return message