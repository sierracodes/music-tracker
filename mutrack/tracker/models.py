"""
models.py

File contains data models for music tracker application.
"""
import datetime
from urllib.parse import quote_plus

from django.db import models
from django.core.exceptions import ValidationError

# For translation--lazy means it's only translated when it's needed
from django.utils.translation import ugettext_lazy as _

# Create your models here.

# No primary key required by default--see
# https://docs.djangoproject.com/en/1.11/topics/db/models/ ...
# ... #automatic-primary-key-fields

# Validators
def validate_zero_to_five(value):
    if value < 0.0 or value > 5.0:
        raise ValidationError(_('Value not between 0 and 5.'))

class PrimaryGenreManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class PrimaryGenre(models.Model):
    """A model representing a particular genre of music.

    These genres will be deliberately broad, so that there are only a handful.
    """
    objects = PrimaryGenreManager()

    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class ArtistManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Artist(models.Model):
    """Model representing an artist.
    """
    objects = ArtistManager()

    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

    def quoted_name(self):
        return quote_plus(self.name)

    class Meta:
        ordering = ('name',)


class Album(models.Model):
    """A model representing an album.
    """
    name = models.CharField(max_length=120)
    year = models.IntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[validate_zero_to_five])
    primary_genres = models.ManyToManyField(PrimaryGenre)
    secondary_genres = models.CharField(max_length=200, blank=True, default='')
    comments = models.TextField(blank=True, default='')
    listen_link = models.URLField(blank=True, default='')

    def __str__(self):
        return self.name

    def artist_name(self):
        return self.artist.name

    def quoted_name(self):
        return quote_plus(self.name)

    class Meta:
        unique_together = ('name', 'artist')
        ordering = ('-rating', 'artist', 'name')


class Listen(models.Model):
    """A model representing an instance of listening to an album.
    """
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    listen_date = models.DateField(default=datetime.date.today, null=True)

    def __str__(self):
        return '{} ({})'.format(self.album, self.listen_date)

    class Meta:
        ordering = ('-listen_date',)
