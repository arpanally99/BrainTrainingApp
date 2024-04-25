
from django.contrib import admin
from django.urls import path,re_path
from quiz_app import views
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_user, name="register"),
    path('login/', views.user_login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('home/', views.home, name="home"),
    path('', views.welcome, name="welcome"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('check-answer/', views.check_answer, name="check-answer"),
    path('profile/', views.profile, name="profile"),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

]
