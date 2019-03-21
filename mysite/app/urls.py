from django.urls import path, include
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
    path('rent_dog/<int:dog_id>', views.rent_dog, name='rent_dog'),
    path('return_dog/<int:dog_id>', views.return_dog, name='return_dog'),
    path('dog_detail/<int:dog_id>', views.dog_detail, name='dog_detail'),
    path('your_dog_list/<int:user_id>', views.your_dog_list, name='your_dog_list'),
    path('edit_dog/<int:dog_id>', views.edit_dog, name='edit_dog'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('edit_user/<int:user_id>', views.edit_user, name='edit_user'),
    path('change_password/', views.change_password, name='change_password'),
    path('add_review/<int:dog_id>', views.add_review, name='add_review'),
    path('are_you_sure/<int:user_id>', views.are_you_sure, name='are_you_sure'),
    path('delete_profile/<int:user_id>', views.delete_profile, name='delete_profile'),
    path('delete_dog/<int:dog_id>', views.delete_dog, name='delete_dog'),
    path('delete_review/<int:review_id>', views.delete_review, name='delete_review'),
    path('search_results/', views.search_results, name='search_results'),
]