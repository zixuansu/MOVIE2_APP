from typing import List, Iterable

from movie.adapters.repository import AbstractRepository
from movie.domain.entities import Actor,Genre,Director,Movie,Review,User


def get_all_movies(repo: AbstractRepository):
	return repo.get_movies()

def search_actor(key,repo: AbstractRepository):
	return repo.get_movies_by_actor(key)

def search_genre(key,repo: AbstractRepository):
	return repo.get_movies_by_genre(key)

def search_director(key,repo: AbstractRepository):
	return repo.get_movies_by_director(key)


