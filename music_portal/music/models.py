from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=[('Band', 'Band'), ('Solo', 'Solo')])
    description = models.TextField()

    def __str__(self):
        return self.name


class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()

    def __str__(self):
        return self.title


class Track(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=50)
    duration = models.IntegerField(help_text="Duration in seconds")
    audio_file = models.FileField(upload_to='tracks/', null=True, blank=True)

    def __str__(self):
        return self.title


class FavoriteArtist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_artists')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='fans')

    def __str__(self):
        return f"{self.user.username} likes {self.artist.name}"


from django.utils.timezone import now

class TrackLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey('Track', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track')


class TrackHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey('Track', on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50, default='played')

    def __str__(self):
        return f"{self.user.username} listened to {self.track.title}"
