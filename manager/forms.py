from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from client.models import Gallery, Sample, Family


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass


class GalleryForm(forms.ModelForm):
  class Meta:
    model = Gallery
    fields = ['img', 'title']


class SampleForm(forms.ModelForm):
  class Meta:
    model = Sample
    fields = ['img', 'name']
       