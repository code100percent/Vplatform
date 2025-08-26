from django.contrib import admin
from django.urls import path , include
from videos_display import views as vd_views
from User import views as u_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_in/',u_views.sign_in_page,name='sign_in'),
    path('register/',u_views.register_page,name='register'),
    path('logout/',u_views.logout_user,name='logout'),
    path('your_videos/',vd_views.your_videos,name='your_videos'),
    path('upload_new/',vd_views.upload,name='upload_video'),
    path('',vd_views.homepage,name='home'),
    path('video/<int:id>/', vd_views.full_video, name='full_video'),
    path('video_api/', include('videos_display.urls')),  # only for api endpoints routing
    path('liked_videos/', vd_views.liked_videos, name='liked_videos'),
    path('saved_videos/', vd_views.show_saved_videos, name='saved_videos'),
    path('trendings/',vd_views.trendings,name='trendings'),
    path('subscription/',vd_views.subscriptions,name='subscriptions'),
    path('history/',vd_views.history,name='history'),
    path('results/',vd_views.search_results,name='results'),
    path('user_info/',vd_views.user_info,name='user_info')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
