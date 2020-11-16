from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import *
from passlib.hash import pbkdf2_sha512


def invalid_credentials(form, field):
	""" Username and password checker """
	username = form.username.data
	password = field.data

	user_object = User.query.filter_by(username=username).first()
	if user_object is None:
		raise ValidationError("Username does not exist.")

	elif not pbkdf2_sha512.verify(password, user_object.password):
		raise ValidationError("Username or Password is incorrect.")

class RegistrationForm(FlaskForm):
	""" Registration Form """
	username = StringField('username', validators=[InputRequired(message="Username Required"), 
		Length(min=4, max=25, message="Username must be between 4 and 25.")])
	password = PasswordField('password', validators=[InputRequired(message="Password Required"), 
		Length(min=4, max=25, message="Password must be between 4 and 25.")])
	confirm_password = PasswordField('confirm_password', validators=[InputRequired(message="Confirm Password Required"),
		EqualTo('password', message='Password must match.')])

	submit_field = SubmitField('Create')

	def validate_username(self, username):
		user_object = User.query.filter_by(username=username.data).first()
		if user_object:
			raise ValidationError("Username already exists. Select a different username.")


class LoginForm(FlaskForm):
	""" Login Form """
	
	username = StringField('username', validators=[InputRequired(message="Username Required")])
	password = PasswordField('password', validators=[InputRequired(message="Password Required"), invalid_credentials])
	submit_field = SubmitField('Login')