from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.views import ArtistViewSet, GenreViewSet, AlbumViewSet, SongViewSet, PlaylistViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'songs', SongViewSet, basename='song')
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)