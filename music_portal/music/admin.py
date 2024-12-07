from django.contrib import admin
from .models import Artist, Album, Track, FavoriteArtist, TrackLike

# Администратор для модели Artist
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')
    search_fields = ('name',)
    list_filter = ('type',)

# Администратор для модели Album
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_year')
    search_fields = ('title',)
    list_filter = ('release_year', 'artist')

# Администратор для модели Track
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'genre', 'duration', 'audio_file')
    search_fields = ('title', 'album__title', 'genre')
    list_filter = ('genre', 'album')

# Администратор для модели FavoriteArtist
class FavoriteArtistAdmin(admin.ModelAdmin):
    list_display = ('user', 'artist')
    search_fields = ('user__username', 'artist__name')

# Администратор для модели TrackLike
class TrackLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'track')
    search_fields = ('user__username', 'track__title')

# Регистрация моделей и админских классов
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(FavoriteArtist, FavoriteArtistAdmin)
admin.site.register(TrackLike, TrackLikeAdmin)
