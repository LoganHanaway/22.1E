import unittest
from app import app, db
from models import User, Post

class BloglyTestCase(unittest.TestCase):
    """Test cases for Blogly application."""

    def setUp(self):
        """Set up test client and sample data."""
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'

        db.drop_all()
        db.create_all()

        # Add a user for testing
        self.user = User(first_name="Test", last_name="User", image_url="https://via.placeholder.com/150")
        db.session.add(self.user)
        db.session.commit()

        # Add a post for the user
        self.post = Post(title="Test Post", content="This is a test post.", user_id=self.user.id)
        db.session.add(self.post)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.remove()
        db.drop_all()

    def test_user_list(self):
        """Test the user list page."""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Test User", resp.data)

    def test_user_detail(self):
        """Test the user detail page."""
        with self.client as c:
            resp = c.get(f"/users/{self.user.id}")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Test User", resp.data)
            self.assertIn(b"Test Post", resp.data)

    def test_add_user(self):
        """Test adding a new user."""
        with self.client as c:
            resp = c.post("/users/new", data={
                'first_name': 'New',
                'last_name': 'User',
                'image_url': 'https://via.placeholder.com/150'
            }, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"New User", resp.data)

    def test_edit_user(self):
        """Test editing an existing user."""
        with self.client as c:
            resp = c.post(f"/users/{self.user.id}/edit", data={
                'first_name': 'Updated',
                'last_name': 'User',
                'image_url': 'https://via.placeholder.com/150'
            }, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Updated User", resp.data)

    def test_delete_user(self):
        """Test deleting a user."""
        with self.client as c:
            resp = c.post(f"/users/{self.user.id}/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(b"Test User", resp.data)

    def test_add_post(self):
        """Test adding a new post."""
        with self.client as c:
            resp = c.post(f"/users/{self.user.id}/posts/new", data={
                'title': 'New Post',
                'content': 'Content for new post.'
            }, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"New Post", resp.data)

    def test_post_detail(self):
        """Test the post detail page."""
        with self.client as c:
            resp = c.get(f"/posts/{self.post.id}")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Test Post", resp.data)

    def test_edit_post(self):
        """Test editing an existing post."""
        with self.client as c:
            resp = c.post(f"/posts/{self.post.id}/edit", data={
                'title': 'Updated Post',
                'content': 'Updated content.'
            }, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Updated Post", resp.data)

    def test_delete_post(self):
        """Test deleting a post."""
        with self.client as c:
            resp = c.post(f"/posts/{self.post.id}/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(b"Test Post", resp.data)

    def test_home_page(self):
        """Test the home page shows recent posts."""
        with self.client as c:
            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Test Post", resp.data)
