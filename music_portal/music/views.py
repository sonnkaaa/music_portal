from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Artist, Album, Track, FavoriteArtist, TrackLike, TrackHistory
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.db.models import Count
from .forms import UserUpdateForm
from .models import FavoriteAlbum
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Album, Comment
from .forms import CommentForm


def index(request):
    artists = Artist.objects.all()
    albums = Album.objects.all()
    return render(request, 'music/index.html', {'artists': artists, 'albums': albums})


def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteArtist.objects.filter(user=request.user, artist=artist).exists()
    return render(request, 'music/artist_detail.html', {'artist': artist, 'is_favorite': is_favorite})


def album_detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    tracks = album.tracks.all()
    comments = album.comments.all().order_by('-created_at')

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteAlbum.objects.filter(user=request.user, album=album).exists()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.album = album
            comment.save()
            return redirect('album_detail', album_id=album.id)
    else:
        form = CommentForm()

    return render(request, 'music/album_detail.html', {
        'album': album,
        'tracks': tracks,
        'is_favorite': is_favorite,
        'comments': comments,
        'form': form,
    })


def track_detail(request, track_id):
    track = get_object_or_404(Track, pk=track_id)
    track.is_liked_by_user = False
    if request.user.is_authenticated:
        track.is_liked_by_user = TrackLike.objects.filter(user=request.user, track=track).exists()
    return render(request, 'music/track_detail.html', {'track': track})


@login_required
def download_track(request, track_id):
    track = get_object_or_404(Track, pk=track_id)
    TrackHistory.objects.create(user=request.user, track=track, action="downloaded")
    response = redirect(track.audio_file.url)
    return response



@login_required
def like_track(request, track_id):
    track = get_object_or_404(Track, pk=track_id)
    like, created = TrackLike.objects.get_or_create(user=request.user, track=track)
    if not created:
        like.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def add_favorite_artist(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    FavoriteArtist.objects.get_or_create(user=request.user, artist=artist)
    return redirect('artist_detail', artist_id=artist_id)


@login_required
def remove_favorite_artist(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    FavoriteArtist.objects.filter(user=request.user, artist=artist).delete()
    return redirect('artist_detail', artist_id=artist_id)


@login_required
def favorite_artists(request):
    favorite_artists = FavoriteArtist.objects.filter(user=request.user)
    favorite_tracks = TrackLike.objects.filter(user=request.user)
    return render(request, "music/favorites.html", {
        "favorite_artists": favorite_artists,
        "favorite_tracks": favorite_tracks
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'music/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        return render(request, 'music/login.html', {'error': 'Invalid username or password'})
    return render(request, 'music/login.html')


def logout_user(request):
    logout(request)
    return redirect('index')


def track_history(request):
    return HttpResponse("Track history placeholder")

def all_artists(request):
    artists = Artist.objects.all()
    return render(request, 'music/all_artists.html', {'artists': artists})

def all_albums(request):
    albums = Album.objects.all()
    return render(request, 'music/all_albums.html', {'albums': albums})


@login_required
def user_profile(request):
    user = request.user
    favorite_artists = FavoriteArtist.objects.filter(user=user)
    favorite_albums = FavoriteAlbum.objects.filter(user=user)
    favorite_tracks = TrackLike.objects.filter(user=user)

    statistics = TrackHistory.objects.filter(user=user).values('track__title', 'action').annotate(count=Count('id'))

    return render(request, 'music/user_profile.html', {
        'user': user,
        'favorite_artists': favorite_artists,
        'favorite_albums': favorite_albums,
        'favorite_tracks': favorite_tracks,
        'statistics': statistics,
    })

@login_required
def user_settings(request):
    user = request.user

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = UserUpdateForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('user_settings')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Сохраняем сессию
                return redirect('user_settings')
    else:
        profile_form = UserUpdateForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'music/user_settings.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })


@login_required
def add_favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    favorite, created = FavoriteAlbum.objects.get_or_create(user=request.user, album=album)
    print(f"Добавление альбома: {album.name}, создано: {created}")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    FavoriteAlbum.objects.filter(user=request.user, album=album).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('album_detail', album_id=comment.album.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'music/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
    album_id = comment.album.id
    comment.delete()
    return redirect('album_detail', album_id=album_id)
