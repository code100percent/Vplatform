from django.shortcuts import render

def homepage(request):
    return render(request,'videos_display\homepage_video_display.html',{})

def your_videos(request):
    return render(request,'videos_display/your_videos.html')


