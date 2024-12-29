from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class BaseModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Изображение")

    class Meta:
        abstract = True

class Artist(BaseModel):
    type = models.CharField(
        max_length=50,
        choices=[('Band', 'Группа'), ('Solo', 'Соло')],
        verbose_name="Тип"
    )

    class Meta:
        verbose_name = "Артист"
        verbose_name_plural = "Артисты"
        ordering = ['name']

    def __str__(self):
        return self.name

class Album(BaseModel):
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name='albums',
        verbose_name="Артист"
    )
    release_year = models.IntegerField(verbose_name="Год выпуска")

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
        ordering = ['release_year', 'name']

    def __str__(self):
        return self.name

class Track(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='tracks',
        verbose_name="Альбом"
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    genre = models.CharField(max_length=50, verbose_name="Жанр")
    duration = models.IntegerField(help_text="Длительность в секундах", verbose_name="Длительность")
    audio_file = models.FileField(upload_to='tracks/', null=True, blank=True, verbose_name="Аудиофайл")

    class Meta:
        verbose_name = "Трек"
        verbose_name_plural = "Треки"
        ordering = ['title']

    def __str__(self):
        return self.title

class FavoriteArtist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_artists',
        verbose_name="Пользователь"
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.SET_NULL,
        null=True,
        related_name='fans',
        verbose_name="Артист"
    )

    class Meta:
        verbose_name = "Избранный артист"
        verbose_name_plural = "Избранные артисты"

    def __str__(self):
        return f"{self.user.username} likes {self.artist.name}"

class FavoriteAlbum(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_albums',
        verbose_name="Пользователь"
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        null=True,
        related_name='fans',
        verbose_name="Альбом"
    )

    class Meta:
        verbose_name = "Избранный альбом"
        verbose_name_plural = "Избранные альбомы"

    def __str__(self):
        return f"{self.user.username} likes {self.album.title}"

class TrackLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        verbose_name="Трек"
    )
    liked_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата лайка")

    class Meta:
        unique_together = ('user', 'track')
        verbose_name = "Лайк трека"
        verbose_name_plural = "Лайки треков"

class TrackHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        verbose_name="Трек"
    )
    listened_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата прослушивания")
    action = models.CharField(max_length=50, default='played', verbose_name="Действие")

    class Meta:
        verbose_name = "История треков"
        verbose_name_plural = "Истории треков"

    def __str__(self):
        return f"{self.user.username} listened to {self.track.title}"

class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Пользователь"
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Альбом"
    )
    content = models.TextField(verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Комментарий от {self.user.username} для {self.album.name}"
