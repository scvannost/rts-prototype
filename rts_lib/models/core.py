from flask_sqlalchemy import SQLAlchemy
from os import environ

POSTGRES_USER, POSTGRES_PASSWORD = environ.get("POSTGRES_USER"), environ.get("POSTGRES_PASSWORD")
POSTGRES_URL, POSTGRES_DATABASE = environ.get("POSTGRES_URL"), environ.get("POSTGRES_DATABASE")
SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DATABASE}"

db = SQLAlchemy()

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return db
