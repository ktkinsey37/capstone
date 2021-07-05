"""User model tests."""

#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Location, Backcast

os.environ['DATABASE_URL'] = "postgresql:///climbing-weather-test"

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Test basics of User model"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Location.query.delete()
        Backcast.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        # User can be created and added
        db.session.add(u)
        db.session.commit()

        # User should have default authority and proper username
        self.assertEqual(u.authority, "user")
        self.assertEqual(u.username, "testuser")

        # User repr method works properly
        self.assertEqual(repr(u), f'<User #{u.id}: testuser, test@test.com>')

        db.session.delete(u)
        db.session.commit()

    def test_user_authority(self):
        """"Does a user with admin work"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            authority="admin"
        )

        # User can be created and added
        db.session.add(u)
        db.session.commit()

        # User should have admin authority
        self.assertEqual(u.authority, "admin")

        db.session.delete(u)
        db.session.commit()


    def test_user_creation_failures(self):
        """Will the creation of users fail when passed incorrect info?"""

        u = User(
            email="",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@email.com",
            username="",
            password="HASHED_PASSWORD"
        )

        u3 = User(
            email="test3@email.com",
            username="testuser",
            password=""
        )

        db.session.add(u)
        db.session.commit()

        # self.assertWarns(SAWarning, db.session.commit)
        # Can we talk about how to deal with assertWarns/Raises?

    def test_user_authentication(self):
        """Does user properly authenticate?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # Checkes if the authentication process works properly and fails properly
        # For some reason this fails
        self.assertEqual(User.authenticate('testuser', 'HASHED_PASSWORD'), u)
        self.assertEqual(User.authenticate('testuse', 'HASHED_PASSWORD'), False)
        self.assertEqual(User.authenticate('testuser', 'HASHED_PASSWOR'), False)

        db.session.delete(u)
        db.session.commit()