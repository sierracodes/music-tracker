
import copy
from urllib.parse import unquote_plus

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Album, Artist, Listen
from .forms import ListenForm, ListenFormForAlbum

class IndexView(LoginRequiredMixin, generic.ListView):
    """Index view for the tracker application.
    """
    template_name = 'tracker/index.html'
    context_object_name = 'album_list'

    def get_queryset(self):
        """Get the list of albums to display by default on the index page.

        """
        return Album.objects.all()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Album-related views ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class AlbumView(LoginRequiredMixin, generic.DetailView):
    """Detail view for an individual album.
    """
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

        querystr = '{artist}+{album}'.format(
            album=self.kwargs['album_name'], artist=self.kwargs['artist_name'])

        youtube_search_link = (f'https://www.youtube.com/results?search_query='
                               f'{querystr}')
        context['youtube_search_link'] = youtube_search_link

        return context


class AlbumCreate(LoginRequiredMixin, generic.edit.CreateView):
    """View for creating a new Album.
    """
    model = Album
    fields = ['name', 'artist', 'year', 'rating', 'primary_genres',
              'secondary_genres', 'comments']
    template_name = 'tracker/generic_form.html'

    def get_context_data(self, **kwargs):
        """Get context data for this view.
        """
        # Call super
        context = super(AlbumCreate, self).get_context_data(**kwargs)
        context['action'] = 'Add'
        context['model_name'] = 'Album'
        return context


class AlbumUpdate(LoginRequiredMixin, generic.edit.UpdateView):
    """View for updating an Album.
    """
    model = Album
    fields = ['name', 'artist', 'year', 'rating', 'primary_genres',
              'secondary_genres', 'comments']
    template_name = 'tracker/generic_form.html'

    def get_object(self):
        """Get the object we're looking for.
        """
        artist_name = unquote_plus(self.kwargs['artist_name'])
        album_name = unquote_plus(self.kwargs['album_name'])
        super_qset = super(AlbumUpdate, self).get_queryset()

        filterset = super_qset.filter(artist__name__iexact=artist_name,
                                      name__iexact=album_name)
        return filterset[0]

    def get_context_data(self, **kwargs):
        """Get context data for this view.
        """
        # Call super
        context = super(AlbumUpdate, self).get_context_data(**kwargs)
        context['action'] = 'Edit'
        context['model_name'] = 'Album'
        return context


#~~~~~~~~~~~~~~~~~~~~~~~~~~~ Artist-related views ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class ArtistView(LoginRequiredMixin, generic.DetailView):
    """Detail view for an Artist.
    """
    model = Artist

    def get_object(self):
        """Get the object we're looking for, using the artist name.
        """
        artist_name = unquote_plus(self.kwargs['artist_name'])
        super_qset = super(ArtistView, self).get_queryset()
        filterset = super_qset.filter(name__iexact=artist_name)

        return filterset[0]

    def get_context_data(self, **kwargs):
        """Get context data for the view.
        """
        # Call super
        context = super(ArtistView, self).get_context_data(**kwargs)

        context['albums_by_artist'] = Album.objects.filter(
            artist__name__iexact=unquote_plus(self.kwargs['artist_name']))

        return context


class ArtistCreate(LoginRequiredMixin, generic.edit.CreateView):
    """View for creating a new Artist.
    """
    model = Artist
    fields = ['name']
    template_name = 'tracker/generic_form.html'

    def get_context_data(self, **kwargs):
        """Get context data for this view.
        """
        # Call super
        context = super(ArtistCreate, self).get_context_data(**kwargs)
        context['action'] = 'Add'
        context['model_name'] = 'Artist'
        return context


class ArtistUpdate(LoginRequiredMixin, generic.edit.UpdateView):
    """View for updating an Artist.
    """
    model = Artist
    fields = ['name']
    template_name = 'tracker/generic_form.html'

    def get_object(self):
        """Get the object we're looking for, using the artist name.
        """
        artist_name = unquote_plus(self.kwargs['artist_name'])
        super_qset = super(ArtistUpdate, self).get_queryset()
        filterset = super_qset.filter(name__iexact=artist_name)

        return filterset[0]

    def get_context_data(self, **kwargs):
        """Get context data for this view.
        """
        # Call super
        context = super(ArtistUpdate, self).get_context_data(**kwargs)
        context['action'] = 'Edit'
        context['model_name'] = 'Artist'
        return context


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Listen-related views ~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class ListenCreate(LoginRequiredMixin, generic.edit.CreateView):
    """View for adding a new Listen.
    """
    model = Listen
    form_class = ListenForm
    template_name = 'tracker/generic_form.html'

    def get_context_data(self, **kwargs):
        """Get context data for this view.
        """
        # Call super
        context = super(ListenCreate, self).get_context_data(**kwargs)

        # Add the action and model name to the context for displaying
        context['action'] = 'Add'
        context['model_name'] = 'Listen'

        return context


class ListenCreateForAlbum(LoginRequiredMixin, generic.edit.CreateView):
    """View for creating a listen for a specific album.
    """
    model = Listen
    form_class = ListenFormForAlbum
    template_name = 'tracker/listen_for_album_form.html'

    def get_context_data(self, **kwargs):
        """Get context data for this view.
        """
        # Call super
        context = super(ListenCreateForAlbum, self).get_context_data(**kwargs)

        # Add the action and model name to the context for displaying
        context['action'] = 'Add'
        context['model_name'] = 'Listen'

        # Add the album name to the context (currently using Album.__str__)
        context['album'] = str(self.get_initial()['album'])

        return context

    def get_initial(self):
        initial = copy.copy(self.initial)
        initial['album'] = Album.objects.get(
            name__iexact=unquote_plus(self.kwargs['album_name']),
            artist__name__iexact=unquote_plus(self.kwargs['artist_name']))
        return initial
