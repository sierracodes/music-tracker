
from urllib.parse import quote_plus, unquote_plus

from django.views import generic

from .models import Album

# Views

class IndexView(generic.ListView):
    template_name = 'tracker/index.html'
    context_object_name = 'album_list'

    def get_queryset(self):
        """Get the list of albums to display by default on the index page.

        """
        return Album.objects.all()


class AlbumView(generic.DetailView):
    model = Album

    def get_object(self):
        """Get the object we're looking for.

        Uses the album_name named group in the URL. Redefined so I don't have
        to use the (meaningless) primary key for the album in the URL.
        """
        artist_name = unquote_plus(self.kwargs['artist_name'])
        album_name = unquote_plus(self.kwargs['album_name'])
        super_qset = super(AlbumView, self).get_queryset()

        filterset = super_qset.filter(artist__name__iexact=artist_name,
                                      name__iexact=album_name)

        return filterset[0]

    def get_context_data(self, **kwargs):
        """Get context data for the view.
        """
        # Call super's method
        context = super(AlbumView, self).get_context_data(**kwargs)

        querystr = '{album}+{artist}'.format(
            album=self.kwargs["album_name"], artist=self.kwargs["artist_name"])

        youtube_search_link = (f'https://www.youtube.com/results?search_query='
                               f'{querystr}')

        context['youtube_search_link'] = youtube_search_link

        return context
