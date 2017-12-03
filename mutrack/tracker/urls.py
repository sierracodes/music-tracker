from django.conf.urls import url

from . import views

app_name = 'tracker'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^album/(?P<artist>[^/\s]+)/(?P<album_name>[^/\s]+)', views.AlbumView.as_view(), name='album')
]
