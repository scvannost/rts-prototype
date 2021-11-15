import flask
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from os import environ
from sqlalchemy.orm.session import Session


POSTGRES_USER, POSTGRES_PASSWORD = environ.get("POSTGRES_USER"), environ.get("POSTGRES_PASSWORD")
POSTGRES_URL, POSTGRES_DATABASE = environ.get("POSTGRES_URL"), environ.get("POSTGRES_DATABASE")
SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DATABASE}"


db = SQLAlchemy()


def init_db(app: flask.Flask) -> SQLAlchemy:
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return db

def with_default_session(f) -> Session:
    """
    For some `f` expecting a database session instance as a keyword argument,
    set the default value of the session keyword argument to the current app's
    database driver's session. We need to do this in a decorator rather than
    inline in the function definition because the current app is only available
    once the app is running and an application context has been pushed.
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        if "session" not in kwargs:
            kwargs["session"] = flask.current_app.extensions["sqlalchemy"].db.session
        return f(*args, **kwargs)

    return wrapped