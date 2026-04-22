from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Movie, Director, Genre

class CreateMovieView(CreateView):
    model = Movie
    template_name = 'moviedb/create.html'
    fields = ['title', 'pub_date', 'directors', 'genres', 'description']
    success_url = reverse_lazy('moviedb:index')


class UpdateMovieView(UpdateView):
    model = Movie
    template_name = 'moviedb/update.html'
    fields = ['title', 'pub_date', 'directors', 'genres', 'description']
    success_url = reverse_lazy('moviedb:index')


class DeleteMovieView(DeleteView):
    model = Movie
    #template_name = 'moviedb/entry_confirm_delete.html'
    success_url = reverse_lazy('moviedb:index')


class IndexView(generic.ListView):
    template_name = 'moviedb/index.html'
    context_object_name = 'latest_movies'
    def get_queryset(self):
        return Movie.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]