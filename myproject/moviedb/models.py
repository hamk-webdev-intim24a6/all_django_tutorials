from django.db import models

class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateField('year published')
    directors = models.ManyToManyField(Director)
    genres = models.ManyToManyField(Genre)
    description = models.TextField(max_length=2000)
    def __str__(self):
        return f"{self.title} ({self.pub_date.year})"
