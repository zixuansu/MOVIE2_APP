import csv
import os
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from movie.adapters.repository import AbstractRepository, RepositoryException
from movie.domain.entities import Actor,Genre,Director,Movie,Review,User,MovieComment,ActorComment,DirectorComment


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._users = list()
        self._movies = list()
        self._genres = set()
        self._actors = set()
        self._directors = set()
        self._movie_comments = list()
        self._director_comments = list()
        self._actor_comments = list()


    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.user_name == username), None)

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        # self._articles_index[article.id] = article

    def get_movie(self, moviename: str) -> Movie:
        movie = None

        try:
            movie = next((movie for movie in self._movies if movie.title == moviename), None)
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    def get_movies_by_actor(self, actorname: str):
        matching_movies = list()
        for movie in self._movies:
            for actor in movie.actors:
                if actorname in actor.name:
                    matching_movies.append(movie)
                    break
        return matching_movies

    def get_movies_by_genre(self, genrename: str) :
        matching_movies = list()
        for movie in self._movies:
            for genre in movie.genres:
                if genrename in genre.name:
                    matching_movies.append(movie)
                    break
        return matching_movies

    def get_movies_by_director(self, directorname: str):
        matching_movies = list()
        for movie in self._movies:
            if directorname in movie.director.name:
                matching_movies.append(movie)
        return matching_movies

    def get_movie_comments(self,moviename):
        matching_comments = list()
        for comment in self._movie_comments:
            if comment['name'] == moviename:
                matching_comments.append(comment)
        return matching_comments

    def add_movie_comment(self,comment: MovieComment):
        self._movie_comments.append(comment)

    def get_director_comments(self,directorname):
        matching_comments = list()
        for comment in self._director_comments:
            if comment['name'] == directorname:
                matching_comments.append(comment)
        return matching_comments

    def add_director_comment(self,comment: DirectorComment):
        self._director_comments.append(comment)

    def get_actor_comments(self,actorname):
        matching_comments = list()
        for comment in self._actor_comments:
            if comment['name'] == actorname:
                matching_comments.append(comment)
        return matching_comments

    def add_actor_comment(self,comment: ActorComment):
        self._actor_comments.append(comment)

    def get_movies(self):
        return self._movies

    def get_genres(self):
        return self._genres

    def get_actors(self):
        return self._actors

    def get_directors(self):
        return self._directors


def read_movie_file(filename: str, repo: MemoryRepository):
    with open(filename, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # movie
            temp_movie = Movie(row['Title'], int(row['Year']))
            temp_movie.description = row['Description']
            # repo.add_movie(temp_movie)

            # directors
            temp_director = Director(row['Director'])
            temp_movie.director = temp_director
            temp_movie.runtime_minutes = int(row['Runtime (Minutes)'])
            repo._directors.add(temp_director)

            # actors
            actor_string = row['Actors']
            for one_actor in actor_string.split(","):
                temp_actor = Actor(one_actor.strip())
                temp_movie.add_actor(temp_actor)
                repo._actors.add(temp_actor)

            # genres
            genre_string = row['Genre']
            for one_genre in genre_string.split(","):
                temp_genre = Genre(one_genre.strip())
                temp_movie.add_genre(temp_genre)
                repo._genres.add(temp_genre)
            
            repo.add_movie(temp_movie)

def read_movie_comment_file(filename: str, repo: MemoryRepository):
    result = []
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append({'name':row['name'],'user':row['user'],'timestamp':row['timestamp'],'text':row['text']})
    repo._movie_comments = result[::-1]

def read_director_comment_file(filename: str, repo: MemoryRepository):
    result = []
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append({'name':row['name'],'user':row['user'],'timestamp':row['timestamp'],'text':row['text']})
    repo._director_comments = result[::-1]

def read_actor_comment_file(filename: str, repo: MemoryRepository):
    result = []
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append({'name':row['name'],'user':row['user'],'timestamp':row['timestamp'],'text':row['text']})
    repo._actor_comments = result[::-1]

def read_user_file(filename: str, repo: MemoryRepository):
    result = []
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append(User(row['user'],row['pwd']))
    repo._users = result

def populate(data_path: str, repo: MemoryRepository):
    movie_filename = os.path.join(data_path, 'Data1000Movies.csv')
    movie_comment_filename = os.path.join(data_path, 'MovieComment.csv')
    director_comment_filename = os.path.join(data_path, 'DirectorComment.csv')
    actor_comment_filename = os.path.join(data_path, 'ActorComment.csv')
    user_filename = os.path.join(data_path, 'user.csv')
    # 
    read_movie_file(movie_filename,repo)
    read_movie_comment_file(movie_comment_filename,repo)
    read_director_comment_file(director_comment_filename,repo)
    read_actor_comment_file(actor_comment_filename,repo)
    read_user_file(user_filename,repo)
