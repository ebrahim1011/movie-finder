from django.urls import path, re_path
from . import views

app_name = 'home'
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]
