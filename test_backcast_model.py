"""Backcast model tests."""



#    python -m unittest test_backcast_model.py


import os
from unittest import TestCase
from models import db, User, Location, Backcast

os.environ['DATABASE_URL'] = "postgresql:///climbing-weather-test"

from app import app

db.create_all()


class BackcastModelTestCase(TestCase):
    """Test model for backcasts."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Location.query.delete()
        Backcast.query.delete()

        self.client = app.test_client()

    def test_backcasts_model(self):
        """Does basic backcast model work?"""

        # Set up user and location to link backcast to
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

        db.session.add(location)
        db.session.commit()

        # Create new backcast
        backcast = Backcast(
                location_id=location.id,
                sun_count=0,
                cloud_count=0,
                precip_count=0,
                total_precip=0,
                avg_precip=0,
                avg_temp=0,
                avg_wind=0,
                high_temp=0,
                high_wind=0)

        # Backcast should link back to location
        self.assertEqual(backcast.location_id, location.id)

        # Ensure that backcast is cascaded when u/location is deleted.
        db.session.delete(u)
        db.session.delete(location)
        db.session.commit()

        # Backcast should cascade when u/location is deleted
        self.assertRaises(TypeError, backcast)