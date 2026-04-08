from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls.base import reverse_lazy
from .models import Dictionary

# index to dictionary app, allowing to search words
def index(request):
    word = ''
    definitions = []
    if 'word' in request.GET:
        word = request.GET['word']
        if len(word)>0:
            definitions = Dictionary.objects.filter(
                word__icontains=word).order_by('word')
    context = {"definitions": definitions}
    return render(request, 'dictionary/index.html', context)

class DictionaryCreateView(CreateView):
    model = Dictionary
    fields = ['word', 'definition']
    template_name = "dictionary/add.html"
    success_url = reverse_lazy('dictionary:add')
    