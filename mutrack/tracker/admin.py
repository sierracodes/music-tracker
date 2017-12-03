from django.contrib import admin

from tracker.models import Artist, Album, PrimaryGenre

# Register your models here.
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(PrimaryGenre)
