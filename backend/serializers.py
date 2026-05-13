from rest_framework import serializers
from .models import Artist, Genre, Album, Song, Playlist, Favorite, PlaylistSong
import datetime

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id','name','slug','bio','image','is_verified']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    artist_name = serializers.ReadOnlyField(source='album.artist.name')
    featured_artists = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    genre = serializers.ReadOnlyField(source='genre.name')
    album_title = serializers.ReadOnlyField(source='album.title')
    formatted_duration = serializers.ReadOnlyField()

    class Meta:
        model = Song
        fields = ['id', 'title','artist_name' ,'album_title', 'genre','featured_artists','audio_file', 'track_number', 'duration_seconds','formatted_duration', 'plays','is_explicit']

class AlbumSerializer(serializers.ModelSerializer):

    artist = ArtistSerializer(read_only=True)
    songs = SongSerializer(many=True, read_only=True)
    song_count = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ['id', 'title', 'slug', 'artist', 'cover_art', 'album_type', 'release_date', 'song_count','total_duration','songs']

    def get_song_count(self, obj):
            return obj.songs.count()

    def get_total_duration(self, obj):
        total_seconds = sum(song.duration_seconds for song in obj.songs.all())
        mins, secs = divmod(total_seconds, 60)
        return f"{mins}:{secs:02d}"


class PlaylistSongSerializer(serializers.ModelSerializer):

    song_title = serializers.ReadOnlyField(source='song.title')
    duration = serializers.ReadOnlyField(source='song.formatted_duration')
    artist_name = serializers.ReadOnlyField(source='song.album.artist.name')

    class Meta:
        model = PlaylistSong
        fields = ['id', 'song', 'song_title','artist_name', 'position', 'added_at', 'duration']

class PlaylistSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    songs = PlaylistSongSerializer(source='playlistsong_set', many=True, read_only=True)
    song_count = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ['id', 'user', 'name', 'description', 'is_public','song_count', 'songs', 'created_at','updated_at']

    def get_song_count(self, obj):
        return obj.songs.count()

class FavoriteSerializer(serializers.ModelSerializer):
    song_title = serializers.ReadOnlyField(source='song.title')

    class Meta:
        model = Favorite
        fields = ['id','user','song','song_title','liked_at']