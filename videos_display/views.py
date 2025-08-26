from django.shortcuts import render,redirect
from .models import Disliked_video, Video ,Liked_video , Comment ,Saved_video, Subscriptions,WatchHistory
from .form import VideoForm
from django.contrib.auth.models import User
#importing JsonResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST


from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import json

def user_info(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'videos_display/user_info.html', {'user': user})
    else:
        return redirect('sign_in')

def homepage(request):
    videos = Video.objects.all()
    return render(request,'videos_display/homepage_video_display.html',{'videos': videos})

def search_results(request):
    query=str(request.GET.get('search_query')).strip().lower()
    query_list = query.split()
    search_results_videos = []
    videos = list(Video.objects.all())
    for video in videos:
        title = video.title.split()
        description = video.description.split()
        username = video.username.split()
        #first preccedence to title
        for q in query_list or q in description or q in username:
            if q in title:
                search_results_videos.append(video)
                break
    return render(request,'videos_display/search_results.html',{'query_videos':search_results_videos})
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
    channel = User.objects.get(username=video.username)
    like_status = False
    dislike_status = False
    is_video_saved = False
    is_video_user_subscribed = False

    if user.is_authenticated:
        # Add to watch history
        from .models import WatchHistory
        WatchHistory.objects.update_or_create(user=user, video=video, defaults={})
        like_status = Liked_video.objects.filter(video=video, user=user).exists()
        dislike_status = Disliked_video.objects.filter(video=video, user=user).exists()
        is_video_saved = Saved_video.objects.filter(video=video, user=user).exists()
        is_video_user_subscribed = Subscriptions.objects.filter(channel=channel, user=user).exists()

    comments = Comment.objects.filter(video=video).order_by('-created_at')
    subscriptions_count = Subscriptions.objects.filter(channel=channel).count()
    context = {
        'video': video,
        'video_liked': like_status,
        'video_disliked': dislike_status,
        'comments': comments,
        'comments_no' : comments.count(),
        'video_saved': is_video_saved,
        'other_videos': Video.objects.exclude(id=video.id).filter(username=video.username),
        'is_video_user_subscribed': is_video_user_subscribed,
        'subscriptions_count': subscriptions_count
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
    if request.user.is_authenticated:
        from .models import WatchHistory, Video
        history_entries = WatchHistory.objects.filter(user=request.user).order_by('-watched_at')
        video_ids = [entry.video.id for entry in history_entries]
        # Preserve order as in history_entries
        videos = list(Video.objects.filter(id__in=video_ids))
        videos_sorted = sorted(videos, key=lambda v: video_ids.index(v.id))
        return render(request, 'videos_display/history_page.html', {'history_videos': videos_sorted})
    else:
        return render(request, 'User/sign_in_request_page.html')
def subscriptions(request):
    if request.user.is_authenticated:
        user = request.user
        # Get all channels the user is subscribed to
        subscriptions = user.subscriptions.select_related('channel').all()
        subscribed_channels = [sub.channel for sub in subscriptions]

        subscribed_videos = Video.objects.filter(username__in=[c.username for c in subscribed_channels]).order_by('-published_date')

        return render(request, 'videos_display/subscriptions.html', {
            'subscribed_channels': subscribed_channels,
            'subscribed_videos': subscribed_videos,
        })
    else:
        return render(request, 'User/sign_in_request_page.html')

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
    

def remove_history(request, video_id):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'not_logged_in'}, status=403)
    try:
        video = Video.objects.get(id=video_id)
        history_entry = WatchHistory.objects.filter(user=user, video=video)
        deleted_count, _ = history_entry.delete()
        if deleted_count:
            return JsonResponse({'message': 'History entry removed successfully'}, status=200)
        else:
            return JsonResponse({'error': 'History entry not found'}, status=404)
    except Video.DoesNotExist:
        return JsonResponse({'error': 'Video not found'}, status=404)




@require_POST
def toggle_subscription(request, video_username):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "not_logged_in"}, status=403)
    channel = User.objects.get(username=video_username)
    if request.user == channel:
        return JsonResponse({"error": "You cannot subscribe to yourself."}, status=400)
    sub = Subscriptions.objects.filter(user=request.user, channel=channel)
    if sub.exists():
        sub.delete()
        subscribed = False
        message = "Unsubscribed successfully"
    else:
        Subscriptions.objects.create(user=request.user, channel=channel)
        subscribed = True
        message = "Subscribed successfully"
    count = Subscriptions.objects.filter(channel=channel).count()
    return JsonResponse({"message": message, "subscriptions_count": count, "subscribed": subscribed})

    

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