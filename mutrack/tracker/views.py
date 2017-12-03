
from urllib.parse import unquote_plus

from django.shortcuts import render
from django.views import generic

from .models import Album

# Views
def index(request):
    return render(request, 'tracker/index.html')


class AlbumView(generic.DetailView):
    model = Album

    def get_object(self):
        """Get the object we're looking for.

        Uses the album_name named group in the URL. Redefined so I don't have
        to use the (meaningless) primary key for the album in the URL.
        """
        artist_name = unquote_plus(self.kwargs['artist'])
        album_name = unquote_plus(self.kwargs['album_name'])
        super_qset = super(AlbumView, self).get_queryset()

        filterset = super_qset.filter(artist__name__iexact=artist_name,
                                      name__iexact=album_name)

        return filterset[0]
