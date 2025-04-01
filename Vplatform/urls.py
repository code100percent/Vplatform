"""
URL configuration for Vplatform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from videos_display import views as vd_views
from User import views as u_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_in',u_views.sign_in_page,name='sign_in'),
    path('register',u_views.register_page,name='register'),
    path('logout',u_views.logout_user,name='logout'),
    path('your_videos',vd_views.your_videos,name='your_videos'),
    path('upload_new',vd_views.upload,name='upload'),
    path('',vd_views.homepage,name='home')
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
