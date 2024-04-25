from django.db import models
from django.contrib.auth.models import User


class OptionChoices(models.TextChoices):
    OPTION_1 = "option1", "Option 1"
    OPTION_2 = "option2", "Option 2"
    OPTION_3 = "option3", "Option 3"
    OPTION_4 = "option4", "Option 4"

class Category(models.TextChoices):
    SCIENCE = "science","Science"
    MATH = "math","Math"
    IQ = "iq","IQ"
    GEOGRAPHY = "geography","Geography"
    SPORTS = "sports",'Sports'

class Type(models.TextChoices):
    PUZZLE = "puzzle","puzzle"
    QUIZ = "quiz","Quiz"


class Question(models.Model):
    category = models.CharField(choices=Category.choices,null=True,blank=True,max_length=50)
    question_text = models.TextField()
    hint = models.TextField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    image = models.ImageField(null=True,blank=True)
    correct_option = models.CharField(max_length=100,choices=OptionChoices.choices)
    type = models.CharField(max_length=100,choices=Type.choices)


    def __str__(self):
        return self.question_text

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_answers = models.IntegerField(default=0)
    total_correct_answers = models.IntegerField(default=0)
    games = models.ManyToManyField(Question,null=True,blank=True)
    correct_answered = models.ManyToManyField(Question,related_name='corrcetly_answered',null=True,blank=True)
    time_taken = models.JSONField(default=list)
    profile_pic = models.ImageField(null=True,blank=True)
    address = models.CharField(max_length=100,blank=True)
    country = models.CharField(max_length=100,blank=True)
    contact = models.CharField(max_length=13,blank=True)
    about_me = models.TextField(null=True,blank=True)


class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True)