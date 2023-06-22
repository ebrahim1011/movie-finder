from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from accounts.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email']


class UserAdminCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email']


class QueryForm(forms.Form):
    query = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'input-w inputsearch'}))


class CheckForm(forms.Form):
    email = forms.EmailField()
