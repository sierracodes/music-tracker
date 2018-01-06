from django.conf.urls import url

from . import views

app_name = 'tracker'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^artist/add/?$', views.ArtistCreate.as_view(), name='artist-create'),
    url(r'^artist/(?P<artist_name>[^/\s]+)', views.ArtistView.as_view(),
        name='artist'),

    url(r'^album/(?P<artist_name>[^/\s]+)/(?P<album_name>[^/\s]+)',
        views.AlbumView.as_view(), name='album')
]
