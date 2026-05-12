from django.db import models
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from .models import Artist, Genre, Album, Song, Playlist, Favorite
from .serializers import (ArtistSerializer, GenreSerializer, AlbumSerializer,SongSerializer, PlaylistSerializer, FavoriteSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from rest_framework.decorators import action
from.permissions import IsOwnerOrReadOnly

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    lookup_field = 'slug'

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.select_related('artist').all()
    serializer_class = AlbumSerializer
    lookup_field = 'slug'

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.select_related('album', 'genre').all()
    serializer_class = SongSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'album__artist__name', 'album__title']
    filterset_fields = ['genre', 'album', 'album__artist']

    @action(detail=True, methods=['post'])
    def increment_plays(self, request, pk=None):
        song = self.get_object()
        song.plays = F('plays') + 1
        song.save(update_fields=['plays'])
        song.refresh_from_db()
        return Response({'status': 'play count updated', 'plays': song.plays})

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Playlist.objects.filter(models.Q(is_public=True) | models.Q(user=user))
        return Playlist.objects.filter(is_public=True)

    def perform_create(self, serializer):
        # Automatically set the user during creation
        serializer.save(user=self.request.user)

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('song')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)