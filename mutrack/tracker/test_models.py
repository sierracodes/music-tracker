"""
Test module for models in the tracker application.
"""

from django.test import TestCase
from django.db.utils import IntegrityError

from .models import Artist


class ArtistTestCase(TestCase):

    def test_unique_name(self):
        """Verify that no two artists can have the same name.
        """
        Artist.objects.create(name='Queen')

        with self.assertRaises(IntegrityError):
            Artist.objects.create(name='Queen')
