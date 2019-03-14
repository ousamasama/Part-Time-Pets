from django.contrib.auth.models import User
from django import forms
from app.models import *
from django.contrib.admin import widgets

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)

class DogForm(forms.ModelForm):

    class Meta:
        model = Dog
        fields = ('name', 'breed', 'description', 'image')
        labels = {'breed': 'Breed'}

class DogEditForm(forms.ModelForm):
  
  class Meta:
    model = Dog
    fields = ('name', 'description', 'image')
    labels = {
      'name': 'Name',
      'description': 'Description',
      'image': 'Image',
    }

class UserEditForm(forms.ModelForm):
  
  class Meta:
    model = User
    fields = ('username', 'email', 'first_name', 'last_name')
    labels = {
      'username': 'Username',
      'first_name': 'First Name',
      'last_name': 'Last Name',
      'email': 'Email'
    }