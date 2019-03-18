from django.contrib.auth.models import User
from django import forms
from app.models import *
from django.contrib.admin import widgets
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

class DateInput(forms.DateInput):
  input_type = 'date'

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

class DogReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('description', 'date')
        labels = {'description': 'Description', 'date': 'Date of Review'}
        widgets = {'date': DateInput(),}

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
            Row(
                Column('old_password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row mb-n2'
            ),
            Row(
                Column('password', css_class='form-group col-md-6 mb-0'),
                Column('confirm_password', css_class='form-group col-md-6 mb-0')
            ),
        )

  class Meta:
      model = User
      fields = ('password',)