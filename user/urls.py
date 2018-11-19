from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView
from .views import register, profile


app_name = 'user'
urlpatterns = [
    path('bootstrap/', TemplateView.as_view(template_name='base.html')),
    path('register/', register, name="register_user"),
    path('login/', auth_views.LoginView.as_view(template_name="user/login.html"), name="login_user"),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name="logout_user"),
    path('profile/', profile, name='profile'),
]