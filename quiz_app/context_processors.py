# context_processors.py

from .models import Notification,UserProgress

def notifications_processor(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user)[:4]
    else:
        notifications = []

    return {'notifications':notifications}

def profile_process(request):
    if request.user.is_authenticated:
        profile = UserProgress.objects.get(user=request.user)
    else:
        profile = None
    return {'profile':profile}