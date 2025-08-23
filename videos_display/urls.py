## these are for video_api views routing only

from django.urls import path
from .views import comment,save_video,remove_like,subscribe ,unsubscribe ,delete_video
urlpatterns = [
    path('comment/<int:video_id>/', comment, name='comment'),
    path('save_video/<int:video_id>/', save_video, name='save_video'),
    path('remove_like/<int:video_id>/', remove_like, name='remove_like'),
    path("subscribe/<int:video_id>/", subscribe, name="subscribe"),
    path("unsubscribe/<int:video_id>/", unsubscribe, name="unsubscribe"),
    path('delete_video/<int:video_id>/', delete_video, name='delete_video')
]