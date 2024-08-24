from django.urls import path

from app import views

urlpatterns = [
    path('login/', views.SpotifyLoginView.as_view(), name='spotify-login'),
    path('profile/', views.SpotifyProfileView.as_view(), name='spotify-profile'),
    path('callback/', views.SpotifyCallbackView.as_view(), name='spotify-callback'),
    path('artist/', views.SpotifyArtistsView.as_view(), name='spotify-artist'),
    path('track/', views.SpotifyTrackView.as_view(), name='spotify-track'),
    path('logout/', views.SpotifyLogoutView.as_view(), name='spotify-logout'),
]
