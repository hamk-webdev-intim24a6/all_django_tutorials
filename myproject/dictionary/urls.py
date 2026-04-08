from django.urls import path

from . import views

app_name = 'dictionary'

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.DictionaryCreateView.as_view(), name="add"),
]
