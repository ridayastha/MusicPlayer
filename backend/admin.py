from django.contrib import admin
from .models import Artist, Genre, Album, Song, Playlist, PlaylistSong, Favorite

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_verified', 'created_at')
    search_fields = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SongInline(admin.TabularInline):
    model = Song
    extra = 1
    fields = ('title', 'genre', 'track_number', 'audio_file')

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album_type', 'release_date')
    list_filter = ('album_type','release_date', 'artist')
    search_fields = ('title', 'artist__name')
    inlines = [SongInline]

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'track_number', 'formatted_duration', 'plays')
    list_filter = ('album', 'genre')
    search_fields = ('title','album__artist__name')
    readonly_fields = ('duration_seconds',)
    raw_id_fields = ('album',)

class PlaylistSongInline(admin.TabularInline):
    model = PlaylistSong
    extra = 1

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_public', 'created_at')
    list_filter = ('is_public','created_at')
    search_fields = ('name', 'user__username')
    inlines = [PlaylistSongInline]

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'liked_at')
    raw_id_fields = ('user', 'song')