from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('description', 'image', 'pub_date', 'mod_date')
    search_fields = ['description']
    list_filter = ['pub_date', 'mod_date']

admin.site.register(Post, PostAdmin)