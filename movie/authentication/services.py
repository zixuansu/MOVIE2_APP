from werkzeug.security import generate_password_hash, check_password_hash

from movie.adapters.repository import AbstractRepository
from movie.domain.entities import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass

def user_register(username: str, password: str, repo: AbstractRepository):
	user = repo.get_user(username)
	messages = {'state':False}
	if user is not None:
		messages['error'] = 'The user has been registered'
		return messages
	else:
		user = User(username, password)
		repo.add_user(user)
		messages['state'] = True
		messages['error'] = 'register successfully'
		return messages
		'''
		with open('./datafiles/user.csv','a+', encoding='utf-8',newline='') as csvfile:    
			writer=csv.writer(csvfile)
			writer.writerow([user,pwd])
		messages['state'] = True
		messages['error'] = 'register successfully'
		return messages
		'''

def authenticate_user(username: str, password: str, repo: AbstractRepository):
	user = repo.get_user(username)
	messages = {'state':False}
	if user is not None:
		if user.password == password:
			messages['state'] = True
			messages['error'] = 'success'
			return messages
		else:
			messages['error'] = 'pwd error'
			return messages
	else:
		messages['error'] = 'user not exist'
		return messages


# ===================================================
# Functions to convert model entities to dictionaries
# ===================================================

def user_to_dict(user: User):
    user_dict = {
        'username': user.username,
        'password': user.password
    }
    return user_dict