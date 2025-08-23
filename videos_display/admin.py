from django.contrib import admin
from .models import Video , Liked_video ,Disliked_video , Comment ,Subscriptions
# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'username', 'published_date')
    search_fields = ('title', 'username')
    ordering = ('-published_date',)
class LikedVideoAdmin(admin.ModelAdmin):
    list_display = ('get_video_id', 'get_username')
    search_fields = ('video__title', 'user__username')

    def get_video_id(self, obj):
        return obj.video.id
    get_video_id.short_description = 'Video ID'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

class DislikedVideoAdmin(admin.ModelAdmin):
    list_display = ('get_video_id', 'get_username')
    search_fields = ('video__title', 'user__username')

    def get_video_id(self, obj):
        return obj.video.id
    get_video_id.short_description = 'Video ID'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'content', 'created_at')
    search_fields = ('user__username', 'video__title', 'content')
    ordering = ('-created_at',)

class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel')
    search_fields = ('user__username', 'channel__username')

admin.site.register(Video, VideoAdmin)
admin.site.register(Liked_video, LikedVideoAdmin)
admin.site.register(Disliked_video, DislikedVideoAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)
admin.site.site_header = "Vplatform Admin"