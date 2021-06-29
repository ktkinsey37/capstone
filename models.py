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
    def signup(cls, username, email, password):
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

class Location(db.Model):
    """A frequently visited climbing location."""

    __tablename__ = 'locations'

    id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False
    )

    user_id = db.Column(
                    db.Integer,
                    db.ForeignKey('users.id', ondelete='CASCADE'),
                    nullable=False
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
                db.Float,
                default=0
    )

    longitude = db.Column(
                db.Float,
                default=0
    )

    image_url = db.Column(
                db.Text,
                default=""
                # need a default image
    )

    description = db.Column(
                db.Text,
                default=""
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

    backcasts = db.relationship('Backcast')

    def __repr__(self):
        return f"<Location #{self.id}: {self.name}. Snowy? {self.is_snowy}, Desert? {self.is_desert}>"

class Backcast(db.Model):
    """A backcast"""

    __tablename__ = 'backcasts'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    location_id = db.Column(
                    db.Integer,
                    db.ForeignKey('locations.id', ondelete='CASCADE'),
                    nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    sun_count = db.Column(
                db.Integer,
                nullable=False
    )

    cloud_count = db.Column(
                db.Integer,
                nullable=False
    )

    precip_count = db.Column(
                    db.Integer,
                    nullable=False
    )

    total_precip = db.Column(
                    db.Float,
                    nullable=False
    )

    avg_precip = db.Column(
                    db.Float,
                    nullable=False
    )

    avg_temp = db.Column(
                    db.Float,
                    nullable=False
    )

    high_temp = db.Column(
                    db.Float,
                    nullable=False
    )

    avg_wind = db.Column(
                    db.Float,
                    nullable=False
    )

    high_wind = db.Column(
                    db.Float,
                    nullable=False
    )

    assessment = db.Column(
                db.Text,
                nullable=False
    )

    user_report = db.Column(
                db.Text,
    )

    location = db.relationship('Location', backref='backcast')

    def __repr__(self):
        return f"<Backcast #{self.id}, {self.sun_count + self.precip_count + self.cloud_count}>"

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
