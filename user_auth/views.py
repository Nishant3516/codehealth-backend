import secrets

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


def github_login(request):
    state = secrets.token_urlsafe(32)
    request.session["github_state"] = state

    url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&state={state}"
        "&scope=read:user user:email"
    )

    return redirect(url)


@api_view(["GET"])
def github_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")

    if state != request.session.get("github_state"):
        return Response({"error": "Invalid state"}, status=400)

    # Exchange code
    token_res = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
        },
        timeout=10,
    )

    token_json = token_res.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return Response({"error": "Token exchange failed"}, status=400)

    # Get profile
    user_res = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    profile = user_res.json()

    # Get email properly
    email_res = requests.get(
        "https://api.github.com/user/emails",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    primary_email = next(
        (e["email"] for e in email_res if e["primary"]),
        None,
    )

    username = profile["login"]

    user, _ = User.objects.get_or_create(
        username=username,
        defaults={"email": primary_email},
    )

    refresh = RefreshToken.for_user(user)

    deep_link = (
        f"http://localhost:54392/#/oauth-success"
        f"?access={refresh.access_token}&refresh={refresh}"
    )

    response = HttpResponse(status=302)
    response["Location"] = deep_link
    return response
