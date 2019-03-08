from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('register', views.register, name='register'),
    path('dogs', views.dogs, name='dogs'),
    path('add_dog', views.add_dog, name='add_dog'),
    path('invalid_login', views.login_user, name='invalid_login'),
]