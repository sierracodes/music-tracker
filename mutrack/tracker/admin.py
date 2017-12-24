from django.contrib import admin

from tracker.models import Artist, Album, PrimaryGenre, Listen

# Register your models here.
admin.site.register(Artist)
admin.site.register(PrimaryGenre)
admin.site.register(Listen)

class AlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist_name', 'year', 'rating']
    search_fields = ['name', 'artist__name']


admin.site.register(Album, AlbumAdmin)
