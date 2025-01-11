from django.urls import path, include
from . import views
from django.conf.urls import handler403, handler404, handler500


handler403 = 'music.views.custom_403'
handler404 = 'music.views.custom_404'
handler500 = 'music.views.custom_500'


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
    path('artists/', views.all_artists, name='all_artists'),
    path('albums/', views.all_albums, name='all_albums'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/settings/', views.user_settings, name='user_settings'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('add_favorite_album/<int:album_id>/', views.add_favorite_album, name='add_favorite_album'),
    path('remove_favorite_album/<int:album_id>/', views.remove_favorite_album, name='remove_favorite_album'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('send-email/', views.send_test_email, name='send_email'),
]
