"""
models.py

File contains data models for music tracker application.
"""
import datetime

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


class Artist(models.Model):
    """Model representing an artist.
    """
    name = models.CharField(max_length=120)

    def __str__(self):
        return '[Artist: {}]'.format(self.name)


class Album(models.Model):
    """A model representing an album.
    """
    name = models.CharField(max_length=120)
    year = models.IntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[validate_zero_to_five])

    def __str__(self):
        return '[Album: {}]'.format(self.name)


class Listen(models.Model):
    """A model representing an instance of listening to an album.
    """
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    listen_date = models.DateField(default=datetime.date.today)
