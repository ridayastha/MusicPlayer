from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from .utils import generate_unique_slug
import mutagen
from django.core.files import File
import math

class Artist(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    image = models.ImageField(upload_to='artists/', default='default_artist.jpg')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Artist, self.name)
        super().save(*args, **kwargs)

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
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    cover_art = models.ImageField(upload_to='covers/')
    album_type = models.CharField(max_length=10, choices=ALBUM_TYPES, default='album')
    release_date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-release_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Album, self.title)
        super().save(*args, **kwargs)

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

    # Track number ensures songs appear in the correct order on the album
    track_number = models.PositiveIntegerField(default=1)

    # Featured artists (Many-to-Many as a song can have multiple features)
    featured_artists = models.ManyToManyField(Artist, related_name='featured_songs', blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    plays = models.PositiveIntegerField(default=0, db_index=True)
    is_explicit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['track_number']
        constraints = [
            models.UniqueConstraint(
                fields=['album', 'track_number'],
                name='unique_track_per_album'
            )
        ]

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        super().save(*args, **kwargs)

        """
        Extract duration only once.
        Works with local + cloud storage.
        """

        if is_new and self.audio_file:

            try:
                self.audio_file.open('rb')

                audio = mutagen.File(self.audio_file)

                if audio and hasattr(audio.info, 'length'):
                    self.duration_seconds = int(
                        audio.info.length
                    )

                    super().save(
                        update_fields=['duration_seconds']
                    )

            except Exception as e:

                print(f"Duration extraction failed: {e}")

            finally:
                self.audio_file.close()

    @property
    def formatted_duration(self):

        mins, secs = divmod(
            self.duration_seconds,
            60
        )

        return f"{mins}:{secs:02d}"

    def __str__(self):
        return self.title


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    songs = models.ManyToManyField(Song, related_name='in_playlists', through='PlaylistSong')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} (by {self.user.username})"

class PlaylistSong(models.Model):

    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position']
        constraints = [
            models.UniqueConstraint(
                fields=['playlist', 'song'],
                name='unique_song_in_playlist'
            )
        ]

    def __str__(self):
        return f"{self.song.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='favorited_by')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')
        ordering = ['-liked_at']

    def __str__(self):
        return f"{self.user.username} likes {self.song.title}"