from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('loginuser', views.LoginView.as_view(), name='login'),
    path('registeruser', views.RegisterView.as_view(), name='register'),
    path('profile', views.FavoriteView.as_view(), name='profile'),
    path('logout', views.logout_view, name='logout')
]
