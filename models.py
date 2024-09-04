"""Models for Blogly."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User model."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String, nullable=False, default='https://via.placeholder.com/150')

    def get_full_name(self):
        """Return full name of the user."""
        return f"{self.first_name} {self.last_name}"

    posts = db.relationship('Post', back_populates='user', cascade="all, delete-orphan", lazy=True)

def connect_db(app):
    """Connect the database to the Flask app."""
    db.app = app
    db.init_app(app)
    app.app_context().push()

class Post(db.Model):
    """Post model."""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tags = db.relationship('Tag', secondary='post_tags', back_populates='posts')
    user = db.relationship('User', back_populates='posts')

    def __repr__(self):
        return f"<Post {self.title} by {self.user_id}>"
    
class Tag(db.Model):
    """Tag model."""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    posts = db.relationship('Post', secondary='post_tags', back_populates='tags')

class PostTag(db.Model):
    """PostTag model (join table for Post and Tag)."""
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
