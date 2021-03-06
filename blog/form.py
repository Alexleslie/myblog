from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SearchForm(forms.Form):
    body = forms.TextInput()


class PostForm(forms.Form):
    body = forms.TextInput()


class CommentForm(forms.Form):
    body = forms.CharField()


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1','password2')
