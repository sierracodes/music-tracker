"""
Test module for models in the tracker application.
"""

from django.test import TestCase
from django.db.utils import IntegrityError

from .models import Artist, Album


class ArtistTestCase(TestCase):
    """Test fixture for the Artist model
    """

    def test_create(self):
        """Test creation of an Artist object
        """
        Artist.objects.create(name='Queen')

    def test_unique_name(self):
        """Verify that no two artists can have the same name
        """
        Artist.objects.create(name='Queen')

        with self.assertRaises(IntegrityError):
            Artist.objects.create(name='Queen')


class AlbumTestCase(TestCase):
    """Test fixture for the Album model
    """

    def test_unique_name_plus_artist(self):
        """Test uniquness constraint of artist+album name
        """
        queen = Artist.objects.create(name='Queen')
        thecure = Artist.objects.create(name='The Cure')

        # Create Queen's Greatest Hits (1981 original)
        Album.objects.create(name='Greatest Hits', year=1981, rating=5,
                             artist=queen)

        # Should not cause an error since Artist is different
        Album.objects.create(name='Greatest Hits', year=2001, rating=4,
                             artist=thecure)

        # Verify that attempting to re-create Queen's Greatest Hits causes an
        # error (even if it is a different year for the US re-release)
        with self.assertRaises(IntegrityError):
            Album.objects.create(name='Greatest Hits', year=1992, rating=5,
                                 artist=queen)

    def test_artist_name(self):
        """Test artist_name method of Album
        """
        queen = Artist.objects.create(name='Queen')
        sheer = Album.objects.create(name='Sheer Heart Attack', year=1974,
                                     rating=5, artist=queen)
        self.assertEqual(sheer.artist_name(), queen.name)
        self.assertEqual(sheer.artist_name(), 'Queen')
