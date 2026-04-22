from django.contrib import admin
from django.db.models import Avg
from .models import Topic, Feedback

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'average_rating')
    search_fields = ['name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(avg_rating=Avg('feedback__rating'))

    def average_rating(self, obj):
        if obj.avg_rating is None:
            return '-'
        return f'{obj.avg_rating:.2f}'

    average_rating.admin_order_field = 'avg_rating'
    average_rating.short_description = 'Average rating'

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('topic', 'rating', 'good', 'bad', 'date')
    list_filter = ['topic', 'date']
    search_fields = ['good', 'bad']

admin.site.register(Topic, TopicAdmin)
admin.site.register(Feedback, FeedbackAdmin)
