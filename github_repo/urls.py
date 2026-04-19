from django.urls import path

from github_repo.views import get_user_repos

urlpatterns = [
    path("repos/", get_user_repos, name="github_user_repo"),
]
