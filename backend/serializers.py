from rest_framework import serializers
from .models import Artist, Genre, Album, Song, Playlist, Favorite
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
    genre = serializers.ReadOnlyField(source='genre.name')
    album_title = serializers.ReadOnlyField(source='album.title')

    class Meta:
        model = Song
        fields = ['id', 'title', 'album_title', 'genre', 'audio_file', 'track_number', 'duration', 'plays']

class AlbumSerializer(serializers.ModelSerializer):

    artist = ArtistSerializer(read_only=True)
    songs = SongSerializer(many=True, read_only=True)
    song_count = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ['id', 'title', 'slug', 'artist', 'cover_art', 'album_type', 'release_date', 'song_count','total_duration','songs']

    def get_total_duration(self, obj):
        total_seconds = 0
        for song in obj.songs.all():
            try:
                m, s = map(int, song.duration.split(':'))
                total_seconds += (m * 60) + s
            except ValueError:
                continue

        mins, secs = divmod(total_seconds, 60)
        return f"{mins}:{secs:02d}"

    def get_song_count(self, obj):
            return obj.songs.count()


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'