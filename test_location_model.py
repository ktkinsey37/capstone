"""Location model tests."""

#    python -m unittest test_location_model.py


import os
from unittest import TestCase
from models import db, User, Location, Backcast

os.environ['DATABASE_URL'] = "postgresql:///climbing-weather-test"

from app import app

db.create_all()


class LocationModelTestCase(TestCase):
    """Test model for Locations"""

    def setUp(self):
        """Create test client, clear databases."""

        User.query.delete()
        Location.query.delete()
        Backcast.query.delete()

        self.client = app.test_client()

    def test_location_model(self):
        """Does basic location work?"""

        # Set up user to link to location
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        location = Location(name="Indian Creek",
                            user_id = u.id,
                            location = "S of Moab, UT",
                            latitude="35.5",
                            longitude="-110.15",
                            is_snowy=False,
                            is_desert=True,
                            description="Sandstone splitters",
                            )

        # Location can be created and added
        db.session.add(location)
        db.session.commit()

        # Location should be linked to a user, and should have necessary information
        self.assertEqual(location.user_id, u.id)
        self.assertEqual(location.latitude, 35.5)
        self.assertEqual(location.is_snowy, False)
        self.assertEqual(location.image_url, "https://images.pexels.com/photos/2335126/pexels-photo-2335126.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=750&w=1260")

        # Location repr method works properly
        self.assertEqual(repr(location), f"<Location #{location.id}: {location.name}. Snowy? {location.is_snowy}, Desert? {location.is_desert}>")

        db.session.delete(u)
        db.session.commit()

        # # Location should cascade when u is deleted
        # self.assertRaises(Exception, location)
        # This throws an error from sqlalchemy called ObjectDeletedError. I can't actually catch this error, because I think I need to import it
        # But I have no idea how to identify where to import it from
