from rest_framework import serializers
from .models import Artist, Genre, Album, Song, Playlist, Favorite

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        # This tells Django to include all fields (name, email, dob, etc.) in the Api
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'