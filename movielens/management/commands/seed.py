import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from django.core.management import BaseCommand, CommandError
from movielens.models import Movie, Audience, Rating, Tag
from django.apps import apps

class Command(BaseCommand):
  help = "MovieLens Data Seeder"

  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.movies = []
      self.audiences = []
      self.ratings = []
      self.tags = []
      self.app_path = apps.get_app_config('movielens').path

  def read_csv_files(self):
    self.stdout.write(self.style.SUCCESS('Start reading csv files...'))
    self.movie_df = self.read_csv_file('movies')
    self.rating_df = self.read_csv_file('ratings')
    self.tag_df = self.read_csv_file('tags')

  def read_csv_file(self, filename):
    try:
      self.stdout.write(self.style.SUCCESS('--Start reading {}.csv...'.format(filename)))
      df = pd.read_csv(self.get_csv_path(filename))
      self.stdout.write(self.style.SUCCESS('--Finished reading {}.csv...'.format(filename)))
      return df
    except Exception as e:
      raise CommandError('Error reading {}.csv!'.format(filename))

  def get_csv_path(self, filename):
    return os.path.join(self.app_path, "management", "commands", filename + ".csv")

  def get_timestamp(self, seconds_to_add):
    date_string = "1970-01-01T00:00:00Z"
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ") + timedelta(seconds=seconds_to_add)

  def parse_movies(self):
    self.stdout.write(self.style.SUCCESS('Cleaning movie table...'))
    Movie.objects.all().delete()
    self.stdout.write(self.style.SUCCESS('Start parsing movies...'))
    movie_objects = []
    for index, row in self.movie_df.iterrows():
      genres = row['genres'].split('|')
      movie_object = Movie(id=row['movieId'], title=row['title'], genres=genres)
      movie_objects.append(movie_object)
    Movie.objects.bulk_create(movie_objects)
    self.stdout.write(self.style.SUCCESS('Finished parsing {} movies...'.format(len(movie_objects))))

  def parse_ratings(self):
    self.stdout.write(self.style.SUCCESS('Cleaning rating table...'))
    Rating.objects.all().delete()
    self.stdout.write(self.style.SUCCESS('Start parsing ratings...'))
    rating_objects = []
    for index, row in self.rating_df.iterrows():
      timestamp = self.get_timestamp(row['timestamp'])
      rating_object = Rating(audience_id=row['userId'], movie_id=row['movieId'], rating=row['rating'], timestamp=timestamp)
      rating_objects.append(rating_object)
    Rating.objects.bulk_create(rating_objects)
    self.stdout.write(self.style.SUCCESS('Finished parsing {} ratings...'.format(len(rating_objects))))

  def parse_tags(self):
    self.stdout.write(self.style.SUCCESS('Cleaning tag table...'))
    Tag.object.all().delete()
    self.stdout.write(self.style.SUCCESS('Start parsing tags...'))
    # self.stdout.write(self.style.SUCCESS('Finished parsing {} tags...'.format(len(movie_objects)))))

  def handle(self, *args, **options):
    self.read_csv_files()
    self.parse_movies()
    self.parse_ratings()
    self.parse_tags()
    self.stdout.write(self.style.SUCCESS('Done.'))
