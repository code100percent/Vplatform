from django.shortcuts import render,redirect
from .models import Disliked_video, Video ,Liked_video , Comment ,Saved_video, Subscriptions
from .form import VideoForm
from django.contrib.auth.models import User
#importing JsonResponse
from django.http import JsonResponse


from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import json


def homepage(request):
    videos = Video.objects.all()
    return render(request,'videos_display/homepage_video_display.html',{'videos': videos})

def your_videos(request):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email

        videos = Video.objects.filter(username=username, email=email)
        return render(request,'videos_display/your_videos.html',{'videos': videos})
    else: 
        return render(request,'User/sign_in_request_page.html')

def liked_videos(request):
    if request.user.is_authenticated:
        liked_videos = Liked_video.objects.filter(user=request.user)
        return render(request, 'videos_display/liked_videos.html', {'liked_videos': liked_videos})
    else:
        return render(request, 'User/sign_in_request_page.html')

def upload(request):
    if request.method == "POST":
        username = request.user.username
        email = request.user.email
        title = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"]
        video_file = request.FILES["video"]
        thumbnail = request.FILES.get("thumbnail")

        try:
            Video.objects.create(
                title=title,
                username=username,
                email=email,
                description=description,
                category=category,
                video=video_file,
                thumbnail=thumbnail
            )
            return JsonResponse({"success": True}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
    
def full_video(request, id):
    video = Video.objects.get(id=id)
    video.views += 1
    video.save()
    user = request.user
    like_status = False
    dislike_status = False
    if user.is_authenticated:
        like_status = Liked_video.objects.filter(video=video, user=user).exists()
        dislike_status = Disliked_video.objects.filter(video=video, user=user).exists()
        is_video_saved = Saved_video.objects.filter(video=video, user=user).exists()

    comments = Comment.objects.filter(video=video).order_by('-created_at')
    context = {
        'video': video,
        'video_liked': like_status,
        'video_disliked': dislike_status,
        'comments': comments,
        'comments_no' : comments.count(),
        'video_saved': is_video_saved,
        'other_videos': Video.objects.exclude(id=video.id).filter(username=video.username)

    }
    return render(request, 'videos_display/TheVideoPage.html', context)

def show_saved_videos(request):
    if request.user.is_authenticated:
        saved_videos = Saved_video.objects.filter(user=request.user)
        return render(request, 'videos_display/saved_videos.html', {'watch_later_videos': saved_videos})
    else:
        return render(request, 'User/sign_in_request_page.html')

def trendings(request):
    return render(request, 'videos_display/trendings_page.html')
def history(request):
    return render(request, 'videos_display/history_page.html')
def subscriptions(request):
    # if request.user.is_authenticated:
    #     subscriptions = Subscriptions.objects.filter(user=request.user)
    #     videos = Video.objects.filter(username=subscriptions.channel.username)
    #     content = {'subscribed_channels': subscriptions}

    return render(request, 'videos_display/subscriptions_page.html' )
    # else:
        # return render(request, 'User/sign_in_request_page.html')

##api views 

def comment(request, video_id):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        content = data.get('content', '')
        user = request.user
        video = Video.objects.get(id=video_id)
        if user.is_authenticated:
            comment = Comment.objects.create(video=video, user=user, content=content)
            return JsonResponse({'message': 'Comment added successfully'}, status=201)
        else: 
            return JsonResponse({'error': 'not_logged_in'}, status=403)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def save_video(request, video_id):
    user = request.user
    video = Video.objects.get(id=video_id)
    if user.is_authenticated:
        is_video_saved = Saved_video.objects.filter(video=video, user=user).exists()
        if not is_video_saved:
            Saved_video.objects.create(user=user, video=video)
            return JsonResponse({'message': 'Video saved successfully'}, status=200)
        else:
            Saved_video.objects.filter(video=video, user=user).delete()
            return JsonResponse({'message': 'Video removed from saved videos'}, status=200)
    else:
        return JsonResponse({'error': 'not_logged_in'}, status=403)
    

def remove_like(request, video_id):
    user = request.user
    video = Video.objects.get(id=video_id)
    if user.is_authenticated:
        liked_video = Liked_video.objects.filter(video=video, user=user)
        liked_video.delete()
        print("Like removed")
        video.likes -= 1
        video.save()
        return JsonResponse({'message': 'Like removed successfully'}, status=200)
    else:
        return JsonResponse({'error': 'not_logged_in'}, status=403)
    

# def subscribe(request, username):
#     #username implies channel name 
#     user = request.user
#     if user.is_authenticated:
#         channel_user = User.objects.get(username=username)
#         if Subscriptions.objects.filter(user=user, channel=channel_user).exists():
#             Subscriptions.objects.filter(user=user, channel=channel_user).delete()
#             return JsonResponse({'message': 'unSubscribed successfully'}, status=204)
#         Subscriptions.objects.create(user=user, channel=channel_user)
#         return JsonResponse({'message': 'Subscribed successfully'}, status=201)
#     else:
#         return JsonResponse({'error': 'not_logged_in'}, status=403)


@login_required
def subscribe(request, video_id):
    """Subscribe the logged-in user to a channel."""
    video = Video.objects.get(id=video_id)
    channel = User.objects.get(username=video.username)

    if request.user == channel:
        return JsonResponse({"error": "You cannot subscribe to yourself."}, status=400)

    subscription, created = Subscriptions.objects.get_or_create(
        user=request.user,
        channel=channel
    )

    if created:
        return JsonResponse({"message": "Subscribed successfully"}, status=201)
    else:
        return JsonResponse({"message": "Already subscribed"}, status=200)


@login_required
def unsubscribe(request, video_id):
    """Unsubscribe the logged-in user from a channel."""
    video = get_object_or_404(Video, id=video_id)
    channel = User.objects.get(username=video.username)
    try:
        subscription = Subscriptions.objects.get(user=request.user, channel=channel)
        subscription.delete()
        return JsonResponse({"message": "Unsubscribed successfully"}, status=204)
    except Subscriptions.DoesNotExist:
        return JsonResponse({"error": "Not subscribed"}, status=404)
    

def delete_video(request, video_id):
    user = request.user
    if user.is_authenticated:
        try :
            video = Video.objects.get(id=video_id)
            if video.username == user.username:
                video.delete()
                return JsonResponse({'message': 'Video deleted successfully'}, status=200)
            else:
                return JsonResponse({'error': 'You do not have permission to delete this video'}, status=403)
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Video not found'}, status=404)
    else:
        return JsonResponse({'error': 'not_logged_in'}, status=403)