from flask import Blueprint, render_template, redirect, url_for, session, request

import movie.authentication.services as services
import movie.adapters.repository as repo

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

# Configure Blueprint.
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')


@authentication_blueprint.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if request.method == 'GET':
		return render_template('./authentication/login.html',form=form)
	user = request.form.get('user')
	pwd = request.form.get('pwd')
	messages = services.authenticate_user(user,pwd,repo.repo_instance)
	if messages['state']:
		session['user_info'] = user
		return redirect('/movieslist/')
	else:
		return render_template('./authentication/login.html',form=form,message=messages['error'])

@authentication_blueprint.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if request.method == 'GET':
		return render_template('./authentication/register.html',form=form)
	user = request.form.get('user')
	pwd = request.form.get('pwd')
	messages = services.user_register(user,pwd,repo.repo_instance)
	if messages['state']:
		session['user_info'] = user
		return redirect('/movieslist/')
	else:
		return render_template('./authentication/register.html',form=form,message=messages['error'])

@authentication_blueprint.route('/logout')
def logout():
	del session['user_info']
	return redirect('/movieslist/')

class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 6 characters, and contain a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(6) \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user = StringField('user', [
        DataRequired(message='Your username is required'),
        Length(min=3, message='Your username is too short')],
        render_kw={'placeholder':'Please enter your account'})
    pwd = PasswordField('pwd', [
        DataRequired(message='Your password is required'),
        PasswordValid()],
        render_kw={'placeholder':'Please enter your password'})
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    user = StringField('user', [
        DataRequired()],
        render_kw={'placeholder':'Please enter your account'})
    pwd = PasswordField('pwd', [
        DataRequired()],
        render_kw={'placeholder':'Please enter your password'})
    submit = SubmitField('Login')