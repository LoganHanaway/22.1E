import unittest
from app import app, db
from models import User

class BloglyTestCase(unittest.TestCase):
    """Test cases for Blogly application."""

    def setUp(self):
        """Set up test client and sample data."""
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'

        db.drop_all()
        db.create_all()

        user = User(first_name="Test", last_name="User", image_url="https://via.placeholder.com/150")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.remove()
        db.drop_all()

    def test_user_list(self):
        """Test the user list page."""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual
