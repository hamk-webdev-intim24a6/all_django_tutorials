from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_text', 'date')
    list_filter = ['date']
    search_fields = ['message_text']

admin.site.register(Message, MessageAdmin)