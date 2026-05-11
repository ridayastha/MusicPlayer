from django.db import models
from django.db.models import Q
from rest_framework import viewsets, permissions
from .models import Artist, Genre, Album, Song, Playlist, Favorite
from .serializers import (ArtistSerializer, GenreSerializer, AlbumSerializer,SongSerializer, PlaylistSerializer, FavoriteSerializer)

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.select_related('artist').all()
    serializer_class = AlbumSerializer

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.select_related('album', 'genre').all()
    serializer_class = SongSerializer

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Playlist.objects.filter(models.Q(is_public=True) | models.Q(user=user))
        return Playlist.objects.filter(is_public=True)

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('song')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)