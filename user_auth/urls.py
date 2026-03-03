from django.urls import path

from user_auth.views import github_callback, github_login

urlpatterns = [
    path("github/login/", github_login, name="github-login"),
    path("github/callback/", github_callback, name="github-callback"),
]
