from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.shortcuts import redirect
import requests
from urllib.parse import urlencode


class SpotifyLoginView(APIView):
    def get(self, request):
        scope = "user-read-private user-read-email"
        params = {
            "response_type": "code",
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
            "scope": scope
        }
        auth_url = f"https://accounts.spotify.com/authorize?{urlencode(params)}"
        return redirect(auth_url)


class SpotifyCallbackView(APIView):
    def get(self, request):
        code = request.GET.get('code')
        token_url = "https://accounts.spotify.com/api/token"
        response = requests.post(
            token_url,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
                'client_id': settings.SPOTIFY_CLIENT_ID,
                'client_secret': settings.SPOTIFY_CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        token_data = response.json()
        access_token = token_data.get('access_token')

        if access_token:
            request.session['spotify_access_token'] = access_token
            return Response({"message": "Authentication successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Authentication failed."}, status=status.HTTP_400_BAD_REQUEST)


class SpotifyProfileView(APIView):
    def get(self, request):
        access_token = request.session.get('spotify_access_token')
        if access_token:
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            response = requests.get("https://api.spotify.com/v1/me", headers=headers)
            if response.status_code == 200:
                profile_data = response.json()
                return Response(profile_data, status=status.HTTP_200_OK)
            return Response({"error": "Failed to fetch profile."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "No access token found."}, status=status.HTTP_401_UNAUTHORIZED)


class SpotifyArtistsView(APIView):
    def get(self, request):
        artist_id = '0TnOYISbd1XYRBk9myaseg'
        access_token = request.session.get('spotify_access_token')
        if access_token:
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            response = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}", headers=headers)
            if response.status_code == 200:
                artists_data = response.json()
                return Response(artists_data, status=status.HTTP_200_OK)
            return Response({"error": "Failed to fetch artists."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "No access token found."}, status=status.HTTP_401_UNAUTHORIZED)


class SpotifyTrackView(APIView):
    def get(self, request):
        track_id = '11dFghVXANMlKmJXsNCbNl'
        access_token = request.session.get('spotify_access_token')
        if access_token:
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            response = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers)
            if response.status_code == 200:
                track_data = response.json()
                return Response(track_data, status=status.HTTP_200_OK)
            return Response({"error": "Failed to fetch track."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "No access token found."}, status=status.HTTP_401_UNAUTHORIZED)


class SpotifyLogoutView(APIView):
    def post(self, request):
        request.session.flush()
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
