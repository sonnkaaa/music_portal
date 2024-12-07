from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('artist/<int:artist_id>/', views.artist_detail, name='artist_detail'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('track/<int:track_id>/', views.track_detail, name='track_detail'),
    path('favorites/', views.favorite_artists, name='favorite_artists'),
    path('like_track/<int:track_id>/', views.like_track, name='like_track'),
    path('track_history/', views.track_history, name='track_history'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('add_favorite_artist/<int:artist_id>/', views.add_favorite_artist, name='add_favorite_artist'),
    path('remove_favorite_artist/<int:artist_id>/', views.remove_favorite_artist, name='remove_favorite_artist'),
    path('download_track/<int:track_id>/', views.download_track, name='download_track'),
    path('favorites/', views.favorite_artists, name='favorites'),
]