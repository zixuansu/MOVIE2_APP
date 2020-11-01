import datetime
import csv
class Actor:
    def __init__(self, name):
        self.name = name
        self.colleaguelist = []

    def __repr__(self):
        if (isinstance(self.name, str) == False):
            return "<Actor None>"
        elif len(self.name) == 0:
            return "<Actor None>"
        else:
            return "<Actor " + self.name + ">"

    def __eq__(self, gname):
        if self.name == gname:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name

    def add_actor_colleague(self, colleague):
        self.colleaguelist.append(colleague)

    def check_if_this_actor_worked_with(self, colleague):
        if colleague in self.colleaguelist:
            return True
        else:
            return False
class Genre:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if len(self.name) != 0:
            return "<Genre " + self.name + ">"
        else:
            return "<Genre None>"

    def __eq__(self, gname):
        if self.name == gname:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name
class Director:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if len(self.name) != 0:
            return "<Director " + self.name + ">"
        else:
            return "<Director None>"

    def __eq__(self, dname):
        if self.name == dname:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name

class Movie:

    def __init__(self, title, release_year):
        if isinstance(title, str):
            self._title = title.strip()
        else:
            self._title = None

        if release_year >= 1900:
            self.release_year = release_year
        else:
            self.release_year = None

        self._description = ""
        self._director = None
        self._actors = []
        self._genres = []
        self._runtime_minutes = 0

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        if isinstance(new_title, str):
            self._title = new_title.strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if isinstance(value, str):
            self._description = value.strip()

    @property
    def director(self):
        return self._director

    @director.setter
    def director(self, value):
        if isinstance(value, Director):
            self._director = value

    @property
    def actors(self):
        return self._actors

    @actors.setter
    def actors(self, new_value):
        if isinstance(new_value, list):
            self._actors = new_value

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, new_value):
        if isinstance(new_value, list):
            self._genres = new_value

    @property
    def runtime_minutes(self):
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, new_value):
        if isinstance(new_value, int):
            if new_value <= 0:
                raise ValueError()

            self._runtime_minutes = new_value

    def __repr__(self):
        return "<Movie " + self._title + ", " + str(self.release_year) + ">"

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False

        if self._title == other.title and self.release_year == other.release_year:
            return True
        return False

    def __lt__(self, other):
        first = self._title + str(self.release_year)
        second = other.title + str(other.release_year)

        return first < second

    def __hash__(self):
        return hash(self._title + str(self.release_year))

    def add_actor(self, actor):
        if isinstance(actor, Actor):
            self._actors.append(actor)

    def remove_actor(self, actor):
        if isinstance(actor, Actor) and actor in self._actors:
            self._actors.remove(actor)

    def add_genre(self, genre):
        if isinstance(genre, Genre):
            self._genres.append(genre)

    def remove_genre(self, genre):
        if isinstance(genre, Genre) and genre in self._genres:
            self._genres.remove(genre)

class Review:
    def __init__(self, movie, review_text, rating):
        self._movie = movie
        self._review_text = review_text

        if 1 <= rating <= 10:
            self._rating = rating
        else:
            self._rating = None
        self._timestamp = datetime.datetime.now().timestamp()

    def __repr__(self):
        return "Review: " + self._review_text + "\n" + "Rating: " + str(self._rating)

    def __eq__(self, other):
        if self._movie == other.movie and self._review_text == other.review_text \
                and self._rating == other.rating and self._timestamp == other.timestamp:
            return True
        return False

    @property
    def movie(self):
        return self._movie

    @property
    def review_text(self):
        return self._review_text

    @property
    def rating(self):
        return self._rating

    @property
    def timestamp(self):
        return self._timestamp

class User:

    def __init__(self, user_name, password):
        self._user_name = user_name.strip().lower()
        self._password = password

        self._watched_movies = []
        self._reviews = []

        self._time_spent_watching_movies_minutes = 0

    @property
    def user_name(self):
        return self._user_name

    @property
    def password(self):
        return self._password

    @property
    def watched_movies(self):
        return self._watched_movies

    @property
    def reviews(self):
        return self._reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self._time_spent_watching_movies_minutes

    def __repr__(self):
        return '<User ' + self._user_name + '>'

    def __eq__(self, other):
        return self._user_name == other.user_name

    def __lt__(self, other):
        return self._user_name < other.user_name

    def __hash__(self):
        return hash(self._user_name)

    def watch_movie(self, movie):
        if isinstance(movie, Movie):
            self._watched_movies.append(movie)
            self._time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review):
        if isinstance(review, Review):
            self._reviews.append(review)

class MovieFileCSVReader:

    def __init__(self, filename):
        self.filename = filename

        self.movies = []
        self.actors = set()
        self.directors = set()
        self.genres = set()

    def read_csv_file(self):
        with open(self.filename, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # movie
                temp_movie = Movie(row['Title'], int(row['Year']))
                temp_movie.description = row['Description']
                # self.movies.append(temp_movie)

                # directors
                temp_director = Director(row['Director'])
                temp_movie.director = temp_director
                temp_movie.runtime_minutes = int(row['Runtime (Minutes)'])
                self.directors.add(temp_director)

                # actors
                actor_string = row['Actors']
                for one_actor in actor_string.split(","):
                    temp_actor = Actor(one_actor.strip())
                    temp_movie.add_actor(temp_actor)
                    self.actors.add(temp_actor)

                # genres
                genre_string = row['Genre']
                for one_genre in genre_string.split(","):
                    temp_genre = Genre(one_genre.strip())
                    temp_movie.add_genre(temp_genre)
                    self.genres.add(temp_genre)
                
                self.movies.append(temp_movie)

    @property
    def dataset_of_movies(self):
        return self.movies

    @property
    def dataset_of_actors(self):
        return self.actors

    @property
    def dataset_of_directors(self):
        return self.directors

    @property
    def dataset_of_genres(self):
        return self.genres

class MovieComment:
    def __init__(self, movie, user, text, timestamp):
        self.movie = movie
        self.user = user
        self.text = text
        self.timestamp = timestamp

    def __repr__(self):
        if len(self.text) != 0:
            return "<MovieComment " + self.text + ">"
        else:
            return "<MovieComment None>"

    def __eq__(self, ctext):
        if self.text == ctext:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.text)

    def __lt__(self, other):
        return self.text < other.text

class ActorComment:
    def __init__(self, actor, user, text, timestamp):
        self.actor = actor
        self.user = user
        self.text = text
        self.timestamp = timestamp

    def __repr__(self):
        if len(self.text) != 0:
            return "<ActorComment " + self.text + ">"
        else:
            return "<ActorComment None>"

    def __eq__(self, ctext):
        if self.text == ctext:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.text)

    def __lt__(self, other):
        return self.text < other.text

class DirectorComment:
    def __init__(self, director, user, text, timestamp):
        self.director = director
        self.user = user
        self.text = text
        self.timestamp = timestamp

    def __repr__(self):
        if len(self.text) != 0:
            return "<DirectorComment " + self.text + ">"
        else:
            return "<DirectorComment None>"

    def __eq__(self, ctext):
        if self.text == ctext:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.text)

    def __lt__(self, other):
        return self.text < other.text
