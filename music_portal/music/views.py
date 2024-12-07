from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Artist, Album, Track, FavoriteArtist, TrackLike, TrackHistory
from django.http import Http404


def index(request):
    artists = Artist.objects.all()
    tracks = Track.objects.all()
    return render(request, 'music/index.html', {'artists': artists, 'tracks': tracks})


def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteArtist.objects.filter(user=request.user, artist=artist).exists()
    return render(request, 'music/artist_detail.html', {'artist': artist, 'is_favorite': is_favorite})


def album_detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/album_detail.html', {'album': album})


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
    return redirect('track_detail', track_id=track_id)


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
