import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_repos(request):
    access_token = request.headers.get("Authorization")
    if not access_token:
        return Response({"error": "No access token provided"}, status=400)

    url = "https://api.github.com/user/repos"
    github_token = request.user.githubprofile.github_token
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    params = {"visibility": "all", "affiliation": "owner"}

    try:
        github_response = requests.get(url, headers=headers, params=params)

        if github_response.status_code == 200:
            return Response(github_response.json())

        return Response(
            {
                "error": "Failed to fetch repositories",
                "details": github_response.json(),
            },
            status=github_response.status_code,
        )

    except requests.exceptions.RequestException as e:
        return Response(
            {"error": "GitHub request failed", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
