import csv
import os

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from movie.domain.entities import Actor,Genre,Director,Movie,Review,User,MovieComment,ActorComment,DirectorComment
from movie.adapters.repository import AbstractRepository

all_genres = None
all_actors = None
all_directors = None

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_user_name=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return user

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, moviename: str) -> Movie:
        movie = None

        try:
            movie = self._session_cm.session.query(Movie).filter(Movie._title==moviename).one()
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    def get_movies_by_actor(self, actorname: str):
        matching_actors_list = self._session_cm.session.query(Actor).filter(Actor.name.like('%'+actorname+'%')).all()
        matching_movies = list()
        for actor in matching_actors_list:
            for movie in actor._actor_movies:
                if movie not in matching_movies:
                    matching_movies.append(movie)
        return matching_movies

    def get_movies_by_genre(self, genrename: str) :
        matching_genres_list = self._session_cm.session.query(Genre).filter(Genre.name.like('%'+genrename+'%')).all()
        matching_movies = list()
        for genre in matching_genres_list:
            for movie in genre._genre_movies:
                if movie not in matching_movies:
                    matching_movies.append(movie)
        return matching_movies

    def get_movies_by_director(self, directorname: str):
        matching_movies = self._session_cm.session.query(Movie).filter(Movie._director.like('%'+directorname+'%')).all()
        return matching_movies

    def get_movie_comments(self,moviename):
        matching_comments = self._session_cm.session.query(MovieComment).filter(MovieComment.movie==moviename).all()
        return matching_comments

    def add_movie_comment(self,comment: MovieComment):
        with self._session_cm as scm:
            scm.session.add(comment)
            scm.commit()

    def get_director_comments(self,directorname):
        matching_comments = self._session_cm.session.query(DirectorComment).filter(DirectorComment.director==directorname).all()
        return matching_comments

    def add_director_comment(self,comment: DirectorComment):
        with self._session_cm as scm:
            scm.session.add(comment)
            scm.commit()

    def get_actor_comments(self,actorname):
        matching_comments = self._session_cm.session.query(ActorComment).filter(ActorComment.actor==actorname).all()
        return matching_comments

    def add_actor_comment(self,comment: dict):
        with self._session_cm as scm:
            scm.session.add(comment)
            scm.commit()

    def get_movies(self):
        movies = self._session_cm.session.query(Movie).all()
        return movies

    def get_genres(self):
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def get_actors(self):
        actors = self._session_cm.session.query(Actor).all()
        return actors

    def get_directors(self):
        directors = self._session_cm.session.query(Director).all()
        return directors

def read_movie_file(filename: str):
    with open(filename, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        movie_id = 0
        genre_id = 0
        actor_id = 0
        director_id = 0
        for row in reader:
            title = row['Title']
            release_year = int(row['Year'])
            description = row['Description']
            director = row['Director']
            runtime_minutes = int(row['Runtime (Minutes)'])
            actors = row['Actors']
            genres = row['Genre']

            # directors
            cur_director_id = None
            if director not in all_directors:
                cur_director_id = director_id
                all_directors.append(director)
                director_id += 1
            else:
                cur_director_id = all_directors.index(director)

            # genres
            cur_genre_id = None
            genres = genres.split(',')
            for genre in genres:
                if genre not in all_genres:
                    cur_genre_id = genre_id
                    all_genres[genre] = list()
                    all_genres[genre].append((cur_genre_id,movie_id))
                    genre_id += 1
                else:
                    cur_genre_id = all_genres[genre][0][0]
                    all_genres[genre].append((cur_genre_id,movie_id))

            # actors
            cur_actor_id = None
            actors = actors.split(',')
            for actor in actors:
                if actor not in all_actors:
                    cur_actor_id = actor_id
                    all_actors[actor] = list()
                    all_actors[actor].append((cur_actor_id,movie_id))
                    actor_id += 1
                else:
                    cur_actor_id = all_actors[actor][0][0]
                    all_actors[actor].append((cur_actor_id,movie_id))

            yield movie_id, title, release_year, description, director, runtime_minutes
            movie_id += 1

def read_movie_comment_file(filename):
    movie_comment_id = 0
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name']
            user = row['user']
            timestamp = row['timestamp']
            text = row['text']
            yield movie_comment_id,name,user,timestamp,text
            movie_comment_id += 1

def read_director_comment_file(filename: str):
    director_comment_id = 0
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name']
            user = row['user']
            timestamp = row['timestamp']
            text = row['text']
            yield director_comment_id,name,user,timestamp,text
            director_comment_id += 1

def read_actor_comment_file(filename: str):
    actor_comment_id = 0
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name']
            user = row['user']
            timestamp = row['timestamp']
            text = row['text']
            yield actor_comment_id,name,user,timestamp,text
            actor_comment_id += 1

def read_user_file(filename: str):
    user_id = 0
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield user_id,row['user'],row['pwd']
            user_id += 1

def generate_movies(filename: str):
    movies = list()
    for movie in read_movie_file(filename):
        movies.append(movie)
    return movies

def generate_director():
    for i in range(len(all_directors)):
        yield i,all_directors[i]

def generate_genre():
    for genre in all_genres:
        yield all_genres[genre][0][0], genre

def generate_actor():
    for actor in all_actors:
        yield all_actors[actor][0][0], actor

def generate_movie_comments(filename: str):
    comments = list()
    for comment in read_movie_comment_file(filename):
        comments.append(comment)
    return comments

def generate_director_comments(filename: str):
    comments = list()
    for comment in read_director_comment_file(filename):
        comments.append(comment)
    return comments

def generate_actor_comments(filename: str):
    comments = list()
    for comment in read_actor_comment_file(filename):
        comments.append(comment)
    return comments

def generate_users(filename: str):
    users = list()
    for user in read_user_file(filename):
        users.append(user)
    return users

def generate_movie_actors():
    movie_actor_id = 0
    for key in all_actors:
        for actor_tuple in all_actors[key]:
            yield movie_actor_id,actor_tuple[1],actor_tuple[0]
            movie_actor_id += 1

def generate_movie_genres():
    movie_genre_id = 0
    for key in all_genres:
        for genre_tuple in all_genres[key]:
            yield movie_genre_id,genre_tuple[1],genre_tuple[0]
            movie_genre_id += 1

def populate(engine: Engine, data_path: str):
    movie_filename = os.path.join(data_path, 'Data1000Movies.csv')
    movie_comment_filename = os.path.join(data_path, 'MovieComment.csv')
    director_comment_filename = os.path.join(data_path, 'DirectorComment.csv')
    actor_comment_filename = os.path.join(data_path, 'ActorComment.csv')
    user_filename = os.path.join(data_path, 'user.csv')

    conn = engine.raw_connection()
    cursor = conn.cursor()

    global all_directors
    global all_genres
    global all_actors
    all_directors = list()
    all_genres = dict()
    all_actors = dict()

    insert_movies = """
        INSERT INTO movies (
        id, title, release_year, description, director, runtime_minutes)
        VALUES (?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, generate_movies(movie_filename))

    insert_directors = """
        INSERT INTO directors (
        id, name)
        VALUES (?, ?)"""
    cursor.executemany(insert_directors, generate_director())

    insert_actors = """
        INSERT INTO actors (
        id, name)
        VALUES (?, ?)"""
    cursor.executemany(insert_actors, generate_actor())

    insert_genres = """
        INSERT INTO genres (
        id, name)
        VALUES (?, ?)"""
    cursor.executemany(insert_genres, generate_genre())

    insert_users = """
            INSERT INTO  users (
            id, username, password)
            VALUES (?, ?, ?)"""
    cursor.executemany(insert_users, generate_users(user_filename))

    insert_movie_genre = """
            INSERT INTO  movie_genres (
            id, movie_id, genre_id)
            VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_genre, generate_movie_genres())

    insert_movie_actor = """
        INSERT INTO movie_actors (
        id, movie_id, actor_id)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_actor, generate_movie_actors())

    insert_movie_comments = """
        INSERT INTO movie_comments (
        id, username, name, timestamp, text)
        VALUES (?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movie_comments, generate_movie_comments(movie_comment_filename))

    insert_director_comments = """
        INSERT INTO director_comments (
        id, username, name, timestamp, text)
        VALUES (?, ?, ?, ?, ?)"""
    cursor.executemany(insert_director_comments, generate_director_comments(director_comment_filename))

    insert_actor_comments = """
        INSERT INTO actor_comments (
        id, username, name, timestamp, text)
        VALUES (?, ?, ?, ?, ?)"""
    cursor.executemany(insert_actor_comments, generate_actor_comments(actor_comment_filename))

    conn.commit()
    conn.close()