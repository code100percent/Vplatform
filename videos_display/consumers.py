import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import F
from channels.db import database_sync_to_async
from .models import Video, Liked_video ,Disliked_video, Comment
class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.video_id = self.scope['url_route']['kwargs']['video_id']
        self.user = self.scope["user"]

        await self.accept()

        self.video_group_name = f"video_{self.video_id}"
        await self.channel_layer.group_add(self.video_group_name, self.channel_name)

        await self.send(text_data=json.dumps({
            'message': f'Connected successfully, video ID: {self.video_id}'
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'like':
            if not self.user.is_authenticated:
                return await self.send(json.dumps({'message': 'not_logged_in'}))

            if not await self.is_video_liked():
                await self.make_video_liked()
                await self.increment_like_count()
                likes = await self.get_like_count()

                # Notify other users about the like
                await self.channel_layer.group_send(self.video_group_name, {
                    'type': 'likes_changed_by_someone',
                    'likes': likes,
                    'action': 'added',
                    'username': self.user.username
                })

            else:
                await self.delete_video_like()
                await self.decrement_like_count()
                likes = await self.get_like_count()

                # Notify other users about the like removal
                await self.channel_layer.group_send(self.video_group_name, {
                    'type': 'likes_changed_by_someone',
                    'likes': likes,
                    'action': 'removed',
                    'username': self.user.username
                })

            

        if action == 'dislike':
            if not self.user.is_authenticated:
                return await self.send(json.dumps({'message': 'not_logged_in'}))

            if not await self.is_video_disliked():
                await self.make_video_disliked()
                await self.increment_dislike_count()
                dislikes = await self.get_dislike_count()

                # Notify other users about the dislike
                await self.channel_layer.group_send(self.video_group_name, {
                    'type': 'dislikes_changed_by_someone',
                    'dislikes': dislikes,
                    'action': 'added',
                    'username': self.user.username
                })

            else:
                await self.delete_video_dislike()
                await self.decrement_dislike_count()
                dislikes = await self.get_dislike_count()

                # Notify other users about the dislike removal
                await self.channel_layer.group_send(self.video_group_name, {
                    'type': 'dislikes_changed_by_someone',
                    'dislikes': dislikes,
                    'action': 'removed',
                    'username': self.user.username
                })
        if action == 'post_comment':
            comment = data.get('content')
            if not self.user.is_authenticated:
                return await self.send(json.dumps({'message': 'not_logged_in'}))

            await self.save_comment(comment)

    async def likes_changed_by_someone(self, event):
        likes = event['likes']
        action = event['action']
        user = event['username']
        same_user = 'True' if user == self.user.username else 'False'

        await self.send(text_data=json.dumps({
            'message': 'like_update',
            'likes': likes,
            'action': action,
            'same_user': same_user
        }))
    
    async def dislikes_changed_by_someone(self, event):
        dislikes = event['dislikes']
        action = event['action']
        user = event['username']
        same_user = 'True' if user == self.user.username else 'False'

        await self.send(text_data=json.dumps({
            'message': 'dislike_update',
            'dislikes': dislikes,
            'action': action,
            'same_user': same_user
        }))


    # Like Functions
    @database_sync_to_async
    def is_video_liked(self):
        return Liked_video.objects.filter(video_id=self.video_id, user=self.user).exists()

    @database_sync_to_async
    def make_video_liked(self):
        Liked_video.objects.create(video_id=self.video_id, user=self.user)

    @database_sync_to_async
    def delete_video_like(self):
        Liked_video.objects.filter(video_id=self.video_id, user=self.user).delete()

    @database_sync_to_async
    def increment_like_count(self):
        Video.objects.filter(id=self.video_id).update(likes=F('likes') + 1)

    @database_sync_to_async
    def decrement_like_count(self):
        Video.objects.filter(id=self.video_id).update(likes=F('likes') - 1)

    @database_sync_to_async
    def get_like_count(self):
        return Video.objects.get(id=self.video_id).likes
    


    # Dislike Functions
    @database_sync_to_async
    def is_video_disliked(self):
        return Disliked_video.objects.filter(video_id=self.video_id, user=self.user).exists()

    @database_sync_to_async
    def make_video_disliked(self):
        Disliked_video.objects.create(video_id=self.video_id, user=self.user)

    @database_sync_to_async
    def delete_video_dislike(self):
        Disliked_video.objects.filter(video_id=self.video_id, user=self.user).delete()

    @database_sync_to_async
    def increment_dislike_count(self):
        Video.objects.filter(id=self.video_id).update(dislikes=F('dislikes') + 1)

    @database_sync_to_async
    def decrement_dislike_count(self):
        Video.objects.filter(id=self.video_id).update(dislikes=F('dislikes') - 1)

    @database_sync_to_async
    def get_dislike_count(self):
        return Video.objects.get(id=self.video_id).dislikes

    #comment save
    @database_sync_to_async
    def save_comment(self, content):
        Comment.objects.create(video_id=self.video_id, user=self.user, content=content)
