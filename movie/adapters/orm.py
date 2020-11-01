from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from movie.domain import entities

metadata = MetaData()


actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), unique=True, nullable=False),
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), unique=True, nullable=False),
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), unique=True, nullable=False),
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('release_year', Integer),
    Column('description', String(1024)),
    Column('director', String(255), nullable=False),
    Column('runtime_minutes', Integer),
)

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

movie_actors = Table(
    "movie_actors", metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('actor_id', ForeignKey('actors.id'))
)

movie_genres = Table(
    "movie_genres", metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

movie_comments = Table(
    "movie_comments", metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), nullable=False),
    Column('name', String(255), nullable=False),
    Column('timestamp', String(255)),
    Column('text', String(1024), nullable=False)
)

actor_comments = Table(
    "actor_comments", metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), nullable=False),
    Column('name', String(255), nullable=False),
    Column('timestamp', String(255)),
    Column('text', String(1024), nullable=False)
)

director_comments = Table(
    "director_comments", metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), nullable=False),
    Column('name', String(255), nullable=False),
    Column('timestamp', String(255)),
    Column('text', String(1024), nullable=False)
)

def map_model_to_tables():
    # user
    mapper(entities.User, users, properties={
        '_user_name': users.c.username,
        '_password': users.c.password,
        # '_movie_comments': relationship(entities.MovieComment, backref='_user'),
        # '_director_comments': relationship(entities.DirectorComment, backref='_user'),
        # '_actor_comments': relationship(entities.ActorComment, backref='_user')
    })
    # movie
    movie_mapper = mapper(entities.Movie, movies, properties={
        '_title': movies.c.title,
        'release_year': movies.c.release_year,
        '_description': movies.c.description,
        '_director': movies.c.director,
        '_runtime_minutes': movies.c.runtime_minutes,
        # '_movie_comments': relationship(entities.MovieComment, backref='_movie')
    })
    # movie comments
    mapper(entities.MovieComment, movie_comments, properties={
        'movie': movie_comments.c.name,
        'user': movie_comments.c.username,
        'text': movie_comments.c.text,
        'timestamp': movie_comments.c.timestamp
        })
    # actor
    mapper(entities.Actor, actors, properties={
        'name': actors.c.name,
        # '_actor_comments': relationship(entities.ActorComment, backref='_actor'),
        '_actor_movies': relationship(
            movie_mapper,
            secondary=movie_actors,
            backref='_actors'
            )
        })
    # actor comments
    mapper(entities.ActorComment, actor_comments, properties={
        'actor': actor_comments.c.name,
        'user': actor_comments.c.username,
        'text': actor_comments.c.text,
        'timestamp': actor_comments.c.timestamp
        })
    # genre
    mapper(entities.Genre, genres, properties={
        'name': genres.c.name,
        '_genre_movies': relationship(
            movie_mapper,
            secondary=movie_genres,
            backref='_genres'
            )
        })
    # director
    mapper(entities.Director, directors, properties={
        'name': directors.c.name,
        # '_director_comments': relationship(entities.DirectorComment, backref='_director'),
        })
    # diretor comments
    mapper(entities.DirectorComment, director_comments, properties={
        'director': director_comments.c.name,
        'user': director_comments.c.username,
        'text': director_comments.c.text,
        'timestamp': director_comments.c.timestamp
        })












