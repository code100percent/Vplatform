from django.shortcuts import render,redirect
from .models import Video
from django.http import HttpResponse
from . import form
def homepage(request):
    return render(request,'videos_display\homepage_video_display.html')

def your_videos(request):
    username = request.user.username
    email = request.user.email
    videos = Video.objects.filter(username=username,email=email)
    return render(request,'videos_display/your_videos.html',{'videos': videos})
def upload(request):
    if request.method == 'POST':
        username = request.user.username
        email = request.user.email
        title = request.POST['title']
        description = request.POST['description']
        category = request.POST['category']
        video = request.POST['file']
        # return HttpResponse(str(video))
        user_video= Video.objects.create(username=username,email=email,
                              title=title,
                              description=description,
                              category=category,video=video)
        
        user_video.save()
        return redirect('your_videos')
    
    # if request.method == 'POST':
    #     form = form.VideoForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         video_instance

    return render(request,'videos_display/uploading_new_video.html')


