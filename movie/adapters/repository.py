import abc
from typing import List
from datetime import date

from movie.domain.entities import Actor,Genre,Director,Movie,Review,User,MovieComment,ActorComment,DirectorComment


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, moviename: str) -> Movie:
        """ Returns a Movie with moviename from the repository.

        If there is no Movie with the given moviename, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actor(self, actorname: str):
        """ Returns a list of Movies that were acted by the actor.

        If there are no Movies on the given actor, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_genre(self, genrename: str) :
        """ Returns a list of Movies with genre.

        If there are no Movies on the given actor, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, directorname: str) :
        """ Returns a list of Movies with director.

        If there are no Movies on the given actor, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_comments(moviename):
        """ Returns a list of movie comments
        
        If there are no comments, return an empty list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie_comment(comment:MovieComment):
        """ 
        Adds a movie Comment to the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_director_comments(directorname):
        """ Returns a list of director comments
        
        If there are no comments, return an empty list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_director_comment(comment:DirectorComment):
        """ 
        Adds a director Comment to the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor_comments(actorname):
        """ Returns a list of actor comments
        
        If there are no comments, return an empty list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor_comment(comment:ActorComment):
        """ 
        Adds a actor Comment to the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies():
        """
        return all movies
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres():
        """
        return all genres
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actors():
        """
        return all actor
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_directors():
        """ 
        return all directors
        """
        raise NotImplementedError




