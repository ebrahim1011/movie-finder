from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .forms import UserRegistrationForm, UserLoginForm, UserCreationForm
from .models import User


class UserRegisterView(View):
    class_form = UserCreationForm

    def get(self, request):
        form = self.class_form
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['email'], cd['password1'])
            return redirect('home:home')
        return redirect('accounts:user_register')



class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'email or password is wrong', 'error')
        return render(request, self.template_name, {'form': form})


class UserLogOutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successsfully', 'success')
        return redirect('home:home')
