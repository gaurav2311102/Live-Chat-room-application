from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async

import json
from django.utils.timesince import timesince
import re



class ChatConsumer(AsyncWebsocketConsumer):
    
    @staticmethod
    def clean_group_name(room_name):
        return re.sub(r"[^a-zA-Z0-9_]", "_", room_name)
      
    async def connect(self):
       
        from .models import Room,Message
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
                'type':'message_add',
                'msg': message['text'],
                'user': message['user__username'],
                'msg_id':message['id'],
                'is_Admin':user.is_superuser,
                'created':(timesince(message['created']) + " ago"),
                'deleted':message['deleted'],
                'edited':message['edited']
            }))
        
        
    async def receive(self,text_data):
        data = json.loads(text_data)

             
        if data['type'] == 'send_message':
            
            message = data['msg']
            
            user = self.scope['user']  

        
            message_id,message_created,deleted,edited = await self.save_message(user, message)
        
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'msg': message,
                    'user': user.username,
                    'msg_id' : message_id,
                    'is_Admin':user.is_superuser,
                    'created':message_created,
                    'deleted':deleted,
                    'edited':edited
                }
            )
       
       
               
        elif data['type'] == 'delete_message':
            message_id = data['message_id']
            await self.delete_message(message_id)
            
            # Notify all clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_delete',
                    'message_id': message_id,
                }
            )
            
        elif data['type'] == "update_message":
            message_id = data["message_id"]
            new_text = data["new_text"]
            success = await self.update_message(message_id, new_text)
            if success:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "message_update",
                        "message_id": message_id,
                        "new_text": new_text,
                    }
                )
                
                
    async def chat_message(self,event):
        
         await self.send(text_data=json.dumps({
            'type':'message_add',
            'msg': event['msg'],
            'user': event['user'],
            'msg_id' : event['msg_id'],
            'is_Admin':event['is_Admin'],
            'created':str(event['created']),
            'deleted':event['deleted'],
            'edited':event['edited']
            
            
        }))
    
    async def message_delete(self, event):
        message_id = event['message_id']
        
        await self.send(text_data=json.dumps({
            
            'type': 'message_delete',
            'msg_id': message_id,
    }))


    async def message_update(self,event):
        message_id = event['message_id']
        
        await self.send(text_data=json.dumps({
            'type':'message_update',
            'msg_id': message_id,
            'new_text':event['new_text']
            
        }))
        
        
        
    @sync_to_async
    def save_message(self, user, message):
        from .models import Room,Message
        room = Room.objects.get(name=self.room_name)
        msg_obj = Message.objects.create(room=room, user=user, text=message)
        return msg_obj.id,timesince(msg_obj.created),msg_obj.deleted,msg_obj.edited
        
    @sync_to_async
    def get_previous_messages(self):
        from .models import Room,Message
        room = Room.objects.get(name=self.room_name)
        return list(Message.objects.filter(room=room).order_by( 'created').values('text', 'user__username','id','created','deleted','edited'))
     

    @sync_to_async
    def delete_message(self, message_id):
        from .models import Room,Message
        message = Message.objects.get(id=message_id)
        message.deleted = True
        message.save()
        
    @sync_to_async
    
    def update_message(self,message_id,new_text):
        from .models import Room,Message
        message = Message.objects.get(id=message_id)
        if message.user == self.scope['user']:
            message.text =  new_text
            message.edited = True
            message.save()  
            return True 
    
    async def disconnect(self, code):
        print("websocket disconnected...")
        print("channel name..." , self.channel_name)
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
        raise StopConsumer