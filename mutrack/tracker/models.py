"""
models.py

File contains data models for music tracker application.
"""
import datetime
from urllib.parse import quote_plus

from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy

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
    """Manager for PrimaryGenre model.
    """
    def get_by_natural_key(self, name):
        """Method to allow identification of a PrimaryGenre by name.

        Otherwise would use primary key, which isn't particularly meaningful.
        Helpful for serialization/fixtures.
        """
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
    """Manager for Artist model.
    """
    def get_by_natural_key(self, name):
        """Method to allow identification of an Artist by name.

        Otherwise would use primary key, which isn't particularly meaningful.
        Helpful for serialization/fixtures.
        """
        return self.get(name=name)


class Artist(models.Model):
    """Model representing an artist.
    """
    objects = ArtistManager()

    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

    def quoted_name(self):
        """Get 'quoted' name using pluses as spaces for use in URLs."""
        return quote_plus(self.name)

    def get_absolute_url(self):
        """Get url to detail page for the model instance.
        """
        return reverse_lazy('tracker:artist',
                            kwargs={'artist_name': self.quoted_name()})

    class Meta:
        ordering = ('name',)


class Album(models.Model):
    """Model representing an album.
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
        return '{} [{}]'.format(self.name, self.artist.name)

    def get_absolute_url(self):
        """Get url to detail page for the model instance.
        """
        return reverse_lazy('tracker:album',
                            kwargs={'album_name': self.quoted_name(),
                                    'artist_name': self.artist.quoted_name()})

    def artist_name(self):
        return self.artist.name

    def quoted_name(self):
        """Get 'quoted' name using pluses as spaces for use in URLs."""
        return quote_plus(self.name)

    def all_listens(self):
        """Return all listens for this album."""
        return self.listen_set.filter(album=self)

    def last_five_listens(self):
        """Return five most recent listens for this album."""
        return self.all_listens()[:5]

    def last_listen(self):
        """Return most recent listen for this album."""
        all_listens = self.all_listens()
        if all_listens:
            return all_listens[0]
        else:
            return None

    def last_listen_date_ymd(self):
        """Return date of most recent listen as a string in YYYY/MM/DD format.

        If no last listen, will return 'No listens'
        """
        last_listen = self.last_listen()
        if last_listen:
            return last_listen.slash_date_ymd()
        else:
            return 'No listens'

    def last_listen_date_mdy(self):
        """Return date of most recent listen as a string in MM/DD/YY format.

        If no last listen, will return 'No listens'
        """
        last_listen = self.last_listen()
        if last_listen:
            return last_listen.slash_date_mdy()
        else:
            return 'No listens'

    def number_of_plays(self):
        """Return number of listens for this album."""
        return len(self.all_listens())

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

    def artist_name(self):
        return self.album.artist_name()

    def album_name(self):
        return self.album.name

    def slash_date_ymd(self):
        """Return listen date in YYYY/MM/DD format.

        If no date, 'Unknown date' is returned.
        """
        if self.listen_date is not None:
            return '{:04d}/{:02d}/{:02d}'.format(self.listen_date.year,
                                                 self.listen_date.month,
                                                 self.listen_date.day)
        else:
            return 'Unknown date'

    def slash_date_mdy(self):
        """Return listen date in MM/DD/YY format.

        If no date, 'Unknown date' is returned.
        """
        if self.listen_date is not None:
            return '{:d}/{:d}/{:02d}'.format(self.listen_date.month,
                                             self.listen_date.day,
                                             self.listen_date.year%100)
        else:
            return 'Unknown date'

    def default_date(self):
        """Return listen date in default datetime.date format.

        If no date, 'Unknown date' is returned.
        """
        if self.listen_date is not None:
            return self.listen_date
        else:
            return 'Unknown date'

    class Meta:
        ordering = ('-listen_date',)
