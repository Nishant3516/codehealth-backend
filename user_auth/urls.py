from django.urls import path

from user_auth.views import github_login

urlpatterns = [
    path("github/login/", github_login, name="github_login"),
]
