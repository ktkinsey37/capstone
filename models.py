"""SQLAlchemy models for Climbing Site."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """A user for the climbing site."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
                db.Text,
                nullable=False,
                unique=True
    )

    email = db.Column(
            db.Text,
            nullable=False,
            unique=True,
    )

    password = db.Column(
            db.Text,
            nullable=False,
    )

    authority = db.Column(
                db.Text,
                nullable=False,
                default="user"
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class SpecialLocation(db.Model):
    """A frequently visited climbing location."""

    __tablename__ = 'special_locations'

    id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
    )

    name = db.Column(
            db.Text,
            nullable=False,
            unique=True
    )

    location = db.Column(
                db.Text,
    )

    latitude = db.Column(
                db.Float
    )

    longitude = db.Column(
                db.Float
    )

    image_url = db.Column(
                db.Text,
                default="",
                # need a default image
    )

    description = db.Column(
                db.Text
    )

    is_desert = db.Column(
                db.Boolean,
                nullable=False,
                default=False
    )

    is_snowy = db.Column(
                db.Boolean,
                nullable=False,
                default=False
    )

    desert_forecasts = db.Column(
                    db.Integer,
                    db.ForeignKey('desert-special-forecasts.id', ondelete='CASCADE'),
    )

    # desert_forecasts = db.relationship('DesertForecast')

    def __repr__(self):
        return f"<Special Location #{self.id}: {self.name}. Snowy? {self.is_snowy}, Desert? {self.is_desert}>"

class Location(db.Model):
    """"""

    __tablename__ = 'locations'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    location = db.Column(
            db.Text
    )

    latitude = db.Column(
                db.Float
    )

    longitude = db.Column(
                db.Float
    )

    image_url = db.Column(
        db.Text,
        default="",
        # need a default image
    )

    description = db.Column(
        db.Text,
    )

class DesertForecast(db.Model):
    """A forecast for a Desert Special Location that may be aggregated from multiple regular forecasts"""

    __tablename__ = 'desert-special-forecasts'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    location_id = db.Column(
                    db.Integer,
                    db.ForeignKey('special-locations.id', ondelete='CASCADE'),
    )
    
    location = db.relationship('SpecialLocation')

# class MountainForecast(db.Model):
#     """A forecast for a Mountain Special Location that may be aggregated from multiple regular forecasts"""

#     __tablename__ = 'mountain-special-forecasts'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     )

#     timestamp = db.Column(
#         db.DateTime,
#         nullable=False,
#         default=datetime.utcnow(),
#     )

#     location_id = db.Column(
#                     db.Integer,
#                     db.ForeignKey('special-locations.id', ondelete='CASCADE'),
#     )

#     location = db.relationship('SpecialLocation')

# class Forecast(db.Model):
#     """A forecast for a user-selected location"""

#     __tablename__ = 'forecasts'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     )

#     timestamp = db.Column(
#         db.DateTime,
#         nullable=False,
#         default=datetime.utcnow(),
#     )

#     location = db.relationship('Location')


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
