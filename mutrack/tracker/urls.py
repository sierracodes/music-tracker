from django.conf.urls import url

from . import views

app_name = 'tracker'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^album/(?P<artist_name>[^/\s]+)/(?P<album_name>[^/\s]+)', views.AlbumView.as_view(), name='album')
]
