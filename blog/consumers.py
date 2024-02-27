import json
from channels.generic.websocket import AsyncWebsocketConsumer


class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "posts_group",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "posts_group",
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['message_type']

        if message_type == 'like':
            post_id = text_data_json['post_id']
            # Implement your logic to update the like count for the post
            # For example, fetch the post, increment the like count, and save
            new_like_count = self.update_like_count(post_id)

            # Broadcast the new like count to all connected clients in the group
            await self.channel_layer.group_send(
                "posts_group",
                {
                    "type": "like_message",
                    "post_id": post_id,
                    "new_like_count": new_like_count,
                }
            )

    async def like_message(self, event):
        # This method handles messages sent to the group
        await self.send(text_data=json.dumps({
            'message_type': 'like',
            'post_id': event['post_id'],
            'new_like_count': event['new_like_count'],
        }))

    # Placeholder for the like updating logic
    def update_like_count(self, post_id):
        # Implement the actual logic here
        # This is just a placeholder function
        new_like_count = 0
        return new_like_count
