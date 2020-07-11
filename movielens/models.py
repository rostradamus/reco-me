from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Movie(models.Model):
  title = models.CharField(max_length=255)
  genres = ArrayField(models.CharField(max_length=255), blank=True)

  def __str__(self):
    return self.name


class Audience(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)

  def __str__(self):
    return '{} {}'.format(self.first_name, self.last_name)


class Rating(models.Model):
  audience = models.ForeignKey(Audience, on_delete=models.CASCADE)
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
  rating = models.FloatField()
  timestamp = models.DateTimeField()

class Tag(models.Model):
  audience = models.ForeignKey(Audience, on_delete=models.CASCADE)
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
  tag = models.CharField(max_length=255)
  timestamp = models.DateTimeField()
