from django.urls import path, re_path
from .views import SignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    re_path(r'^logout/$', auth_views.LoginView.as_view(), name="logout")
]