from django.contrib import admin

from tracker.models import Artist, Album, PrimaryGenre

# Register your models here.
admin.site.register(Artist)
admin.site.register(PrimaryGenre)

class AlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist_name', 'year']

admin.site.register(Album, AlbumAdmin)
