from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Artist(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='artists/', default='default_artist.jpg')
    is_verified = models.BooleanField(default=False)  # Added for professional feel

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    ALBUM_TYPES = (
        ('single', 'Single'),
        ('album', 'Album'),
        ('ep', 'EP'),
    )
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=200)
    cover_art = models.ImageField(upload_to='covers/')
    album_type = models.CharField(max_length=10, choices=ALBUM_TYPES, default='album')
    release_date = models.DateField()

    def __str__(self):
        return f"{self.title} by {self.artist.name}"


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='songs')
    title = models.CharField(max_length=200)

    # Added FileExtensionValidator for security/integrity
    audio_file = models.FileField(
        upload_to='music/',
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'm4a'])]
    )

    # Track number ensures songs appear in the correct order in the album
    track_number = models.PositiveIntegerField(default=1)

    # Featured artists (Many-to-Many as a song can have multiple features)
    featured_artists = models.ManyToManyField(Artist, related_name='featured_songs', blank=True)

    duration = models.CharField(max_length=10)
    plays = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['track_number']  # Auto-sorts songs by album order

    def __str__(self):
        return self.title


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    songs = models.ManyToManyField(Song, related_name='in_playlists', blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (by {self.user.username})"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='favorited_by')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')
        ordering = ['-liked_at']

    def __str__(self):
        return f"{self.user.username} likes {self.song.title}"