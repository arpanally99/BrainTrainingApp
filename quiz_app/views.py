from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from . import models
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.


def welcome(request):
    return render(request,'welcome.html')

def register_user(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        if User.objects.filter(username=username).exists():
            error = "Username is taken"
            return render(request,'register.html',{'error':error})
        user=User.objects.create_user(username=username, password=password, 
                                         first_name=first_name, last_name=last_name, 
                                         email=email)
        models.UserProgress.objects.create(user=user)
        return redirect('login')
    return render(request,'register.html',{'error':error})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            models.Notification.objects.create(user=request.user,body='You just logged in.')
        return redirect('home')
    return render(request,'login.html')

@login_required
def home(request):
    # Get a random question from the database
    random_question = models.Question.objects.order_by('?').first()
    return render(request, 'home.html', {'question': random_question})

@login_required
def check_answer(request):
    if request.method == 'POST':
        # Get the user's answer from the POST data
        user_answer = request.POST.get('answer')
        
        question_id = request.POST.get('question_id')
        time_taken = float(request.POST.get('elapsed_time'))/1000.0
        print(request.user)
        user_progress = models.UserProgress.objects.get(user=request.user)
        user_progress.total_answers += 1
        correct_answer = models.Question.objects.get(pk=question_id).correct_option
        if correct_answer == user_answer:
            user_progress.score += 1
            user_progress.total_answers +=1
            user_progress.total_correct_answers +=1
            user_progress.time_taken.append(time_taken)
            user_progress.games.add(models.Question.objects.get(pk=question_id))
            user_progress.correct_answered.add(models.Question.objects.get(pk=question_id))
            user_progress.save()
            body = 'You earned a point.'
            models.Notification.objects.create(user=request.user,body=body)
            response_data = {'result': 'correct'}

        else:
            user_progress.total_answers +=1
            user_progress.games.add(models.Question.objects.get(pk=question_id))
            hint = models.Question.objects.get(pk=question_id).hint
            response_data = {'result': 'incorrect', 'hint': hint}
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user_progress = models.UserProgress.objects.get(user=request.user)
    user_games = user_progress.games.all()

    total_time_taken = 0
    total_games = user_games.count()

    for time in user_progress.time_taken:
        total_time_taken += time

    average_time_taken = total_time_taken / len(user_progress.time_taken)

    science_count = user_games.filter(category=models.Category.SCIENCE).count()
    math_count = user_games.filter(category=models.Category.MATH).count()
    iq_count = user_games.filter(category=models.Category.IQ).count()
    geography_count = user_games.filter(category=models.Category.GEOGRAPHY).count()
    sports_count = user_games.filter(category=models.Category.SPORTS).count()
    quiz = user_games.filter(type=models.Type.QUIZ).count()
    puzzle = user_games.filter(type=models.Type.PUZZLE).count()

    data = {
        'science':science_count,
        'math':math_count,
        'iq':iq_count,
        'geography':geography_count,
        'sports':sports_count,
        'time_taken':user_progress.time_taken,
        'quiz':quiz,
        'puzzle':puzzle,
    }
    return render(request,'dashboard.html',{'user_progress':user_progress,'average_time_taken':average_time_taken,
                                            'user_games':total_games,'data':data})

@login_required
def profile(request):
    profile = models.UserProgress.objects.get(user=request.user)
    user_games = profile.games.all().count()
    url = 'profile'
    # game_count = user_games.count()
    if request.method == 'POST':
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        country = request.POST.get('country')
        about_me = request.POST.get('about_me')
        profile_pic_uploaded = request.FILES.get('profile_pic')
        if profile_pic_uploaded:
            profile_pic = profile_pic_uploaded
        else:
            profile_pic = None
        user = models.User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        profile.address = address
        profile.contact = contact
        profile.country = country
        profile.profile_pic = profile_pic
        profile.about_me = about_me
        profile.save()
        return redirect("profile")
    return render(request,'profile.html',{'profile':profile,'user_games':user_games,'url':url})