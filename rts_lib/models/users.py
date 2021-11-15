from passlib.hash import pbkdf2_sha256
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm.session import Session
from typing import Optional, Tuple

from .core import db, with_default_session

class User(db.Model):
    __table_name__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)

    @classmethod
    @with_default_session
    def get_by_username(cls, username: str, *, session: Session) -> Optional["User"]:
        """
        Returns the userID for a given username.
        str @username
        """
        return session.query(User).filter_by(username=username).first()

    @classmethod
    @with_default_session
    def login(cls, username: str, password: str, *, session: Session) -> Tuple[Optional["User"], Optional[str]]:
        """
        Login a user
        Returns User instance or None, error as str or None
                If no error occured, error is None. Else it is a short description of the error.
                If the username cannot be found, user is None. Else it is the User instance.

        str @username
        str @password
        """
        user : Optional[cls] = cls.get_by_username(username, session=session)
        error = None

        if user is None:
            error = f"Username {username} was not found."
        elif user and not pbkdf2_sha256.verify(password, user.password):
            error = "Incorrect password."
        else: # if user and pbkdf2_sha256.verify(password, user.password):
            # if they both exist and verify, then we're all good
            pass


        return user, error

    @classmethod
    @with_default_session
    def signup(cls, username: str, password: str, email: str, *, session: Session, **kwargs) -> Optional[str]:
        """
        Adds a new user to the users table of the db.
        Returns a str desciprion of the error if one occurred.

        str @username; checked for uniqueness
        str @password
        str @email
        Any **kwargs; checks that they are valid columns of User
        """
        error = None

        if cls.get_by_username(username, session=session):
            error = "Username already taken. Please try a different name."

        for k in kwargs:
            if not k in User.__table__.columns:
                error = "At least one kwarg is invalid."

        if not error:
            new_user = User(
                username=username,
                password=pbkdf2_sha256.hash(password),
                email=email,
                **kwargs,
            )

            try:
                session.add(new_user)
                session.commit()
            except Exception:
                error = "An error occurred in signup, please try again later."

        return error