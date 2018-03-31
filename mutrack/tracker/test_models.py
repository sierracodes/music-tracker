"""
Test module for models in the tracker application.
"""

from django.test import TestCase
from django.db.utils import IntegrityError

import datetime

from .models import Artist, Album, Listen


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


class ListenTestCase(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(name='Queen')
        self.album = Album.objects.create(name='A Day At The Races', year=1976,
                                          rating=5, artist=self.artist)

    def test_create(self):
        """Test creation of a Listen object
        """
        # Create with datetime date
        Listen.objects.create(album=self.album,
                              listen_date=datetime.date(2017, 3, 13))

        # Create with no date, verify defaults to today
        l = Listen.objects.create(album=self.album)
        self.assertEqual(l.listen_date, datetime.date.today())

        # Create with None as date, verify that it works and listen_date stays
        # as None
        l = Listen.objects.create(album=self.album, listen_date=None)
        self.assertEqual(l.listen_date, None)

    def test_slash_date_mdy(self):
        """Test slash_date_mdy method of Listen
        """
        # One-digit month, two-digit day
        listen = Listen.objects.create(album=self.album,
                                       listen_date=datetime.date(2016, 5, 12))
        self.assertEqual(listen.slash_date_mdy(), '5/12/16')

        # Two-digit month, one-digit day
        listen = Listen.objects.create(album=self.album,
                                       listen_date=datetime.date(2016, 11, 1))
        self.assertEqual(listen.slash_date_mdy(), '11/1/16')

        # Test for unknown date
        listen = Listen.objects.create(album=self.album, listen_date=None)
        self.assertEqual(listen.slash_date_mdy(), 'Unknown date')

    def test_slash_date_ymd(self):
        """Test slash_date_mdy method of Listen
        """
        # One-digit month, two-digit day
        listen = Listen.objects.create(album=self.album,
                                       listen_date=datetime.date(2016, 5, 12))
        self.assertEqual(listen.slash_date_ymd(), '2016/05/12')

        # Two-digit month, one-digit day
        listen = Listen.objects.create(album=self.album,
                                       listen_date=datetime.date(2014, 11, 1))
        self.assertEqual(listen.slash_date_ymd(), '2014/11/01')

        # Test for unknown date
        listen = Listen.objects.create(album=self.album, listen_date=None)
        self.assertEqual(listen.slash_date_ymd(), 'Unknown date')

    def test_default_date(self):
        """Test default_date method of Listen
        """
        date = datetime.date(2016, 5, 12)
        listen = Listen.objects.create(album=self.album, listen_date=date)
        self.assertEqual(listen.default_date(), date)

        # Unknown date
        listen = Listen.objects.create(album=self.album, listen_date=None)
        self.assertEqual(listen.default_date(), 'Unknown date')

    def test_sorting(self):
        """Test default sorting behavior of Listens
        """
        # Create some listens with some arbitrary unordered dates
        dates = [
            datetime.date(2014, 11, 1),
            datetime.date(2017, 4, 12),
            datetime.date(2017, 4, 11),
            datetime.date(1987, 6, 30),
            datetime.date(2018, 2, 7)]

        listens = []
        for date in dates:
            listens.append(
                Listen.objects.create(album=self.album, listen_date=date))

        # Verify that when we ask for all of the Listens, they're returned in
        # order of date, newest first
        sorted_listens = sorted(
            listens, key=lambda l: l.listen_date, reverse=True)
        for i, listen in enumerate(Listen.objects.all()):
            self.assertEqual(listen, sorted_listens[i])

        # Add some listens that are different albums and verify everything is
        # still returned in listen order
        opera = Album.objects.create(name='A Night At The Opera', year=1975,
                                     rating=5, artist=self.artist)
        listens.append(Listen.objects.create(
            album=opera, listen_date=datetime.date(1979, 4, 11)))
        listens.append(Listen.objects.create(
            album=opera, listen_date=datetime.date(2018, 12, 10)))

        sorted_listens = sorted(
            listens, key=lambda l: l.listen_date, reverse=True)
        for i, listen in enumerate(Listen.objects.all()):
            self.assertEqual(listen, sorted_listens[i])
