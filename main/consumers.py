from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async
from .models import Room,Message
import json
from django.utils.timesince import timesince
import re


class ChatConsumer(AsyncWebsocketConsumer):
    
    @staticmethod
    def clean_group_name(room_name):
        return re.sub(r"[^a-zA-Z0-9_]", "_", room_name)
      
    async def connect(self):
       
        await self.accept()
        print("websokcet connected...")
        print("channel name..." , self.channel_name)
       
        self.room_name = self.scope['url_route']['kwargs']['roomname']
        
        self.room_group_name = f"chat_{self.clean_group_name(self.room_name)}"
        print("groupname:" ,self.room_group_name)
        
        user = self.scope['user']
        
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        
        messages = await self.get_previous_messages()
        for message in messages:
           
            await self.send(text_data=json.dumps({
                'msg': message['text'],
                'user': message['user__username'],
                'msg_id':message['id'],
                'is_Admin':user.is_superuser,
                'updated':(timesince(message['updated']) + " ago")
            }))
        
        
    async def receive(self,text_data):
        data = json.loads(text_data)
        message = data['msg']
        
        user = self.scope['user']  

       
        message_id,message_updated = await self.save_message(user, message)
        print("message_updated " ,message_updated)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'msg': message,
                'user': user.username,
                'message_id' : message_id,
                'is_Admin':user.is_superuser,
                'updated':message_updated
            }
        )
       
    async def chat_message(self,event):
        
         await self.send(text_data=json.dumps({
            'msg': event['msg'],
            'user': event['user'],
            'message_id' : event['message_id'],
            'is_Admin':event['is_Admin'],
            'updated':str(event['updated'])
            
            
        }))
    
    @sync_to_async
    def save_message(self, user, message):
        
        room = Room.objects.get(name=self.room_name)
        msg_obj = Message.objects.create(room=room, user=user, text=message)
        return msg_obj.id,timesince(msg_obj.updated)
        
    @sync_to_async
    def get_previous_messages(self):
       
        room = Room.objects.get(name=self.room_name)
        return list(Message.objects.filter(room=room).order_by( 'created').values('text', 'user__username','id','updated'))
     
   
    
    async def disconnect(self, code):
        print("websocket disconnected...")
        print("channel name..." , self.channel_name)
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
        raise StopConsumer