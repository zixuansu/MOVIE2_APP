from movie.adapters.repository import AbstractRepository


def add_comment_to_movie(comment,repo: AbstractRepository):
	repo.add_movie_comment(comment)

def add_comment_to_director(comment,repo: AbstractRepository):
	repo.add_director_comment(comment)

def add_comment_to_actor(comment,repo: AbstractRepository):
	repo.add_actor_comment(comment)

def get_all_movies(repo: AbstractRepository):
	return repo.get_movies()

def select_movie(title,repo: AbstractRepository):
	return repo.get_movie(title)

def load_movie_comment(title,repo: AbstractRepository):
	return repo.get_movie_comments(title)

def load_director_comment(name,repo: AbstractRepository):
	return repo.get_director_comments(name)

def load_actor_comment(name,repo: AbstractRepository):
	return repo.get_actor_comments(name)