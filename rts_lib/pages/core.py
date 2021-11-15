import flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from typing import Callable, List

from ..models import User

blueprint = flask.Blueprint(
    "rts",
    __name__,
	static_folder="static",
	template_folder="templates",
	url_prefix="/rts",
)
session = Session()

def init_session(app: flask.Flask, db: SQLAlchemy = None):
	app.config["SESSION_TYPE"] = "sqlalchemy"
	if db:
		app.config["SESSION_SQLALCHEMY"] = db
	if app.secret_key:
		app.config["SESSION_USE_SIGNER"] = True
	session.init_app(app)

# ----------------- Wrappers ----------------- # this must be first

def loggedin(user_list: List[str] = None):
	"""Decorator to check if is logged in"""
	if type(user_list) is str:
		user_list = [user_list]

	def anyone(func: Callable):
		@wraps(func)

		def func_wrapper(*args, **kwargs):
			if "user" in flask.session and isinstance(flask.session["user"], User):
				return func(*args, **kwargs)
			else:
				return fourohone()
		return func_wrapper

	def wrapper(func: Callable):
		@wraps(func)

		def func_wrapper(*args, **kwargs):
			if "user" in flask.session and isinstance(flask.session["user"], User):
				if flask.session["user"].username in user_list:
					return func(*args, **kwargs)
				else:
					return fourohthree()
			else:
				return fourohone()
		return func_wrapper

	if not type(user_list) is list or not user_list[0]:
		return anyone
	else:
		return wrapper


# -------------- Error Handling -------------- #

@blueprint.errorhandler(401)
def fourohone():
	# flask.render_template("401.html")
	return flask.redirect("/login")

@blueprint.errorhandler(403)
def fourohthree():
	return flask.render_template("403.html")


# ------------- User Management -------------- #

@blueprint.route("/login/", methods=["GET","POST"])
def login_page():
	if flask.request.method == "GET":
		if "user" in flask.session and isinstance(flask.session["user"], User):
			return f"logged in as {flask.session['user'].username}"
		else:
			return flask.render_template("login.html")
	elif flask.request.method == "POST":
		username = str(flask.request.form["username"])
		password = str(flask.request.form["password"])

		# initial checks
		error = None
		if not 3 <= len(username) < 20:
			error = "Username must be between 3 and 20 characters."
		elif 6 >= len(password):
			error = "Password must be at least 6 characters."

		# processing
		if not error:
			user, error = User.login(username, password)
		
		# output
		if error:
			return flask.render_template("login.html", error=error)
		else:
			flask.session["user"] = user
			return f"logged in as {flask.session['user'].username}"


@blueprint.route("/logout/", methods=["GET"])
def logout_page():
	if "user" in flask.session:
		flask.session.pop("user")
	return "logged out"


@blueprint.route("/signup/", methods=["GET","POST"])
def signup_page():
	if flask.request.method == "GET":
		return flask.render_template("signup.html")
	elif flask.request.method == "POST":
		username = str(flask.request.form["username"])
		password = str(flask.request.form["password"])
		email = str(flask.request.form["email"])
		confirm = str(flask.request.form["confirm"])
		
		# initial checks
		error = None
		if not 3 <= len(username) < 20:
			error = "Username must be between 3 and 20 characters."
		elif len(email.split("@")) != 2 or len(email.split("@")[1].split(".")) == 1:
			error = "Incorrectly formatted email."
		elif len(email) >= 50:
			error = "Email too long."
		elif password != confirm:
			error = "Passwords do not match."
		elif 6 >= len(password):
			error = "Password must be at least 6 characters."

		if not any([str(i) in password for i in range(10)]):
			error = "Password must contain a number"
		elif not any([i in password for i in ",./<>?;':\"[]\\{}|`~!@#$%^&*()-=_+"]):
			error = "Password must contain one of ,./<>?;':\"[]\\{}|`~!@#$%^&*()-=_+"
		elif password.upper() == password or password.lower() == password:
			error = "Password must contain at least one uppercase and one lowercase letter"
		
		# processing
		if not error:
			error = User.signup(username=username, password=password, email=email)

		# outputs
		if error:
			return flask.render_template("signup.html", data=flask.request.form, error=error)
		else:
			return flask.redirect("/login/")
