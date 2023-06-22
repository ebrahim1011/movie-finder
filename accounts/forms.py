from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('password does not match')
        return cd['password2']
    
    def save(self, commit: True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="you can change password by using <a href=\"../password/\">this form</a>")

    class Meta:
        model = User
        fields = ('email', 'password', 'last_login')


class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email is already exists')
        return email


class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
