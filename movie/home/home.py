from flask import Blueprint, render_template, session, request, redirect

from math import ceil

import movie.adapters.repository as repo
from movie.domain.entities import Actor,Genre,Director,Movie,Review,User
import movie.home.services as services

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/',methods=['GET'])
def index():
	return redirect('/movieslist/')

@home_blueprint.route('/movieslist/<int:page>',methods=['GET'])
@home_blueprint.route('/movieslist/',methods=['GET'])
def watchlist(page=1,key=None,search=None):
	user = session.get('user_info')
	if not user:
		user = None
	movies = services.get_all_movies(repo.repo_instance)
	movies_count = len(movies)
	pages = get_pages(movies_count,per_page=10,cur_page=page)
	# page from 1 to xxx
	cur_page_movies = movies[pages['start_index']:pages['end_index']+1]
	return render_template('./home/movieslist.html',movieslist=cur_page_movies,pages=pages,user=user,endpoint='home_bp.watchlist')

@home_blueprint.route('/movieslist/search/<int:page>',methods=['GET','POST'])
@home_blueprint.route('/movieslist/search/',methods=['GET','POST'])
def searchlist(page=1):
	user = session.get('user_info')
	if not user:
		user = None
	# page from 1 to xxx
	movies = services.get_all_movies(repo.repo_instance)

	if request.method == 'GET':
		key = session.get('key')
		search = session.get('search')
	else:
		key = request.form.get('key')
		search = request.form.get('search')
		session['key'] = key
		session['search'] = search

	if search == 'actor':
		movies = services.search_actor(key,repo.repo_instance)
		movies_count = len(movies)
		pages = get_pages(movies_count,per_page=10,cur_page=page)
	elif search == 'genre':
		movies = services.search_genre(key,repo.repo_instance)
		movies_count = len(movies)
		pages = get_pages(movies_count,per_page=10,cur_page=page)
	else:
		movies = services.search_director(key,repo.repo_instance)
		movies_count = len(movies)
		pages = get_pages(movies_count,per_page=10,cur_page=page)
	# page from 1 to xxx
	cur_page_movies = movies[pages['start_index']:pages['end_index']+1]
	return render_template('./home/movieslist.html',movieslist=cur_page_movies,pages=pages,user=user,endpoint='home_bp.searchlist')

def get_pages(item_count,per_page=10,cur_page=1):
	pages = {}
	last_page = ceil(item_count/per_page)
	if cur_page < last_page:
		pages['start_index'] = (cur_page-1)*per_page
		pages['end_index'] = cur_page*per_page - 1
	elif cur_page == last_page:
		pages['start_index'] = (cur_page-1)*per_page
		pages['end_index'] = item_count - 1
	else:
		pages['start_index'] = (last_page-1)*per_page
		pages['end_index'] = item_count - 1
	pages['per_page'] = per_page
	pages['cur_page'] = cur_page
	pages['last_page'] = last_page
	return pages