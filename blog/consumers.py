from channels.generic.websocket import AsyncWebsocketConsumer
import json


class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['message_type']

        if message_type == 'like':
            post_id = text_data_json['post_id']
            # Process the like (e.g., increment like count in the database)
            new_like_count = ...  # Your logic to get the new like count

            # Broadcast the new like count to all connected clients
            await self.channel_layer.group_send(
                "posts_group",
                {
                    "type": "like_message",
                    "post_id": post_id,
                    "new_like_count": new_like_count,
                }
            )

    # Custom handler for like_message events
    async def like_message(self, event):
        await self.send(text_data=json.dumps({
            'message_type': 'like',
            'post_id': event['post_id'],
            'new_like_count': event['new_like_count'],
        }))
