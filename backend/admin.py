from django.contrib import admin
from .models import Artist, Genre, Album, Song, Playlist, Favorite

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    # You must list specific field names here
    list_display = ('name', 'is_verified')
    search_fields = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album_type', 'release_date')
    list_filter = ('album_type', 'artist')

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'track_number', 'duration', 'plays')
    list_filter = ('album', 'genre')
    search_fields = ('title',)

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_public', 'created_at')
    list_filter = ('is_public',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin): # Fixed spelling to match your Model
    list_display = ('user', 'song', 'liked_at')