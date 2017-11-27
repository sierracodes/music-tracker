from django.conf.urls import url

from . import views

app_name = 'tracker'
urlpatterns = [
    url('^$', views.index, name='index'),
]
