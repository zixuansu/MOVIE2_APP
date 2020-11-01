import datetime

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session, request

import movie.adapters.repository as repo
import movie.detail.services as services
from movie.domain.entities import MovieComment,ActorComment,DirectorComment


# Configure Blueprint.
detail_blueprint = Blueprint('detail_bp', __name__,url_prefix='/detail')

@detail_blueprint.route('/movie/<string:title>/',methods=['GET','POST'])
def show_movie(title):
	user = session.get('user_info')
	if not user:
		user = 'tourist'
	if request.method == 'POST':
		moviename = request.form.get('movie')
		username = request.form.get('user')
		timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%m')
		text = request.form.get('comment')
		comment = MovieComment(moviename,username,timestamp,text)
		if text != '':
			services.add_comment_to_movie(comment,repo.repo_instance)
			# with open('./datafiles/MovieComment.csv','a+', encoding='utf-8',newline='') as csvfile:    
				# writer=csv.writer(csvfile)
				# writer.writerow([moviename,username,timestamp,text])
	movies = services.get_all_movies(repo.repo_instance)
	movie = services.select_movie(title,repo.repo_instance)
	comments = services.load_movie_comment(movie.title,repo.repo_instance)
	return render_template('/detail/movie.html',movie=movie,user=user,comments=comments)

@detail_blueprint.route('/director/<string:name>/',methods=['GET','POST'])
def show_director(name):
	user = session.get('user_info')
	if not user:
		user = 'tourist'
	if request.method == 'POST':
		directorname = request.form.get('director')
		username = request.form.get('user')
		timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%m')
		text = request.form.get('comment')
		comment = DirectorComment(directorname,username,timestamp,text)
		if text != '':
			services.add_comment_to_director(comment,repo.repo_instance)
	comments = services.load_director_comment(name,repo.repo_instance)
	return render_template('/detail/director.html',director=name,user=user,comments=comments)

@detail_blueprint.route('/actor/<string:name>/',methods=['GET','POST'])
def show_actor(name):
	user = session.get('user_info')
	if not user:
		user = 'tourist'
	if request.method == 'POST':
		actorname = request.form.get('actor')
		username = request.form.get('user')
		timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%m')
		text = request.form.get('comment')
		comment = ActorComment(actorname,username,timestamp,text)
		if text != '':
			repo.repo_instance.add_actor_comment(comment)
			# services.add_comment_to_actor(comment,repo.repo_instance)
			# with open('./datafiles/ActorComment.csv','a+', encoding='utf-8',newline='') as csvfile:    
			# 	writer=csv.writer(csvfile)
			# 	writer.writerow([actorname,username,timestamp,text])
	# actors = repo.repo_instance._actors
	# actor = select_actor(actors,name)
	comments = services.load_actor_comment(name,repo.repo_instance)
	return render_template('/detail/actor.html',actor=name,user=user,comments=comments)
