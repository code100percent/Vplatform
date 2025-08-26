from django.db import models
from django.contrib.auth.models import User

#import for thumbnail generation
import os 
from moviepy import VideoFileClip
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

import datetime

class Video(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    published_date = models.DateField(auto_now=True)
    category = models.CharField(max_length=25)
    video = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    duration = models.CharField(max_length=8, blank=True, null=True)  # in seconds

    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save video first

        if self.video:
            video_path = self.video.path
            clip = VideoFileClip(video_path)

            # set duration if not already saved
            if not self.duration:
                duration = clip.duration  # in seconds
                self.duration = str(datetime.timedelta(seconds=int(duration)))

            # create thumbnail if not already saved
            if not self.thumbnail:
                frame = clip.get_frame(clip.duration / 2)  # Get a frame at the middle of the video
                image = Image.fromarray(frame)

                thumb_io = BytesIO()
                image.save(thumb_io, format="JPEG")

                thumb_name = os.path.splitext(os.path.basename(self.video.name))[0] + ".jpg"
                self.thumbnail.save(thumb_name, ContentFile(thumb_io.getvalue()), save=False)

            super().save(update_fields=['duration', 'thumbnail'])



class Liked_video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'video')


class Disliked_video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'video')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Saved_video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'video')

class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')


class Subscriptions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions"   # who I subscribed to
    )
    channel = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribers"     # who subscribed to me
    )

    class Meta:
        unique_together = ('user', 'channel')

    def save(self, *args, **kwargs):
        if self.user == self.channel:
            raise ValueError("A user cannot subscribe to themselves.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} → {self.channel.username}"
    

