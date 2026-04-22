from django.urls import path
from . import views

app_name = 'moviedb'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.CreateMovieView.as_view(), name='create'),
    path('<int:pk>/delete/', views.DeleteMovieView.as_view(), name='delete'),
    path('<int:pk>/', views.UpdateMovieView.as_view(), name='update'),
]


