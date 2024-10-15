import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']

        if user.is_authenticated:
            await self.accept()

            self.group_name = f'notifications_{user.id}'
            print(f"group_name from consumers.py is {self.group_name}")
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
        else:
            await self.close()



    async def disconnect(self, close_code):
        user = self.scope['user']

        if user.is_authenticated or hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )


    async def send_notification(self, event):
        print("Sending notification")
        await self.send(text_data=json.dumps(
            {
                'title': event['title'],
                'message': event['message'],
                'level': event['level'],
            }
        ))
