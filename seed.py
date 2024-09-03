from app import db
from models import User, Post
from datetime import datetime, timezone

# Clear existing data
db.drop_all()
db.create_all()

# Create users
users = [
    User(first_name="Alice", last_name="Smith", image_url="https://via.placeholder.com/150"),
    User(first_name="Bob", last_name="Johnson", image_url="https://via.placeholder.com/150"),
    User(first_name="Carol", last_name="Williams", image_url="https://via.placeholder.com/150"),
    User(first_name="David", last_name="Jones", image_url="https://via.placeholder.com/150"),
    User(first_name="Eve", last_name="Brown", image_url="https://via.placeholder.com/150")
]

db.session.add_all(users)
db.session.commit()

# Create posts
posts = []
titles = [
    "First Post", "Second Post", "Third Post", "Fourth Post", "Fifth Post",
    "Sixth Post", "Seventh Post", "Eighth Post", "Ninth Post", "Tenth Post",
    "Eleventh Post", "Twelfth Post", "Thirteenth Post", "Fourteenth Post", "Fifteenth Post",
    "Sixteenth Post", "Seventeenth Post", "Eighteenth Post", "Nineteenth Post", "Twentieth Post"
]

for i in range(20):
    post = Post(
        title=titles[i],
        content=f"This is the content of post {i+1}.",
        created_at=datetime.now(timezone.utc),
        user_id=users[i % len(users)].id
    )
    posts.append(post)

db.session.add_all(posts)
db.session.commit()
