from django.contrib.auth.models import User
from django import forms
from app.models import *
from django.contrib.admin import widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field

class DateInput(forms.DateInput):
  input_type = 'date'

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
          'username',
          'email',
          'password',
          'first_name',
          'last_name',
        )

class DogForm(forms.ModelForm):

    class Meta:
        model = Dog
        fields = ('name', 'breed', 'description', 'image')
        labels = {'breed': 'Breed'}

    def __init__(self, *args, **kwargs):
        super(DogForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
          'name',
          'breed',
          'description',
          'image',
        )

class DogReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('description', 'date')
        labels = {'description': 'Description', 'date': 'Date of Review'}
        widgets = {'date': DateInput(),}
    
    def __init__(self, *args, **kwargs):
        super(DogReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
          'description',
          'date',
        )

class DogEditForm(forms.ModelForm):
  
  class Meta:
    model = Dog
    fields = ('name', 'description', 'image')
    labels = {
      'name': 'Name',
      'description': 'Description',
      'image': 'Image',
    }
  
  def __init__(self, *args, **kwargs):
        super(DogEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
          Field('name', style='width: 15%;'),
          Field('description', style='width: 50%;'),
          Field('image',),
        )

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
  
  def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
          Field('username', style='width: 15%;'),
          Field('first_name', style='width: 15%;'),
          Field('last_name', style='width: 15%;'),
          Field('email', style='width: 20%;'),
        )

class ChangePassword(forms.ModelForm):
  old_password = forms.CharField(widget=forms.PasswordInput(), label='Old password')
  password = forms.CharField(widget=forms.PasswordInput(), label='Password (at least 8 characters)')
  confirm_password=forms.CharField(widget=forms.PasswordInput(),  label='Confirm new password')

  def clean(self):
      cleaned_data = super(ChangePassword, self).clean()
      password = cleaned_data.get('password')
      confirm_password = cleaned_data.get('confirm_password')

      if password != confirm_password:
          raise forms.ValidationError('')

  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
          'old_password',
          'password',
          'confirm_password'
        )

  class Meta:
      model = User
      fields = ('password',)