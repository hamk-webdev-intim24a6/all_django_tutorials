from django.contrib import admin
from .models import Director, Genre, Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'pub_date')
    list_filter = ['pub_date', 'genres']
    search_fields = ['title', 'description']


class DirectorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    search_fields = ['first_name', 'last_name']


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


admin.site.register(Movie, MovieAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Genre, GenreAdmin)