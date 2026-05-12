from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.views import ArtistViewSet, GenreViewSet, AlbumViewSet, SongViewSet, PlaylistViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)
router.register(r'playlists', PlaylistViewSet)
router.register(r'favorites', FavoriteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)