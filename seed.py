from app import app, db
from models import User, Post, Tag
from datetime import datetime

# Ensure the code runs within an application context
with app.app_context():
    db.drop_all()
    db.create_all()

    # Create users
    user1 = User(first_name="John", last_name="Doe", image_url="https://via.placeholder.com/150")
    user2 = User(first_name="Jane", last_name="Smith", image_url="https://via.placeholder.com/150")
    user3 = User(first_name="Alice", last_name="Johnson", image_url="https://via.placeholder.com/150")
    user4 = User(first_name="Bob", last_name="Brown", image_url="https://via.placeholder.com/150")
    user5 = User(first_name="Charlie", last_name="Davis", image_url="https://via.placeholder.com/150")

    db.session.add_all([user1, user2, user3, user4, user5])
    db.session.commit()

    # Create posts
    post1 = Post(title="First Post", content="Content for first post", created_at=datetime.now(), user_id=user1.id)
    post2 = Post(title="Second Post", content="Content for second post", created_at=datetime.now(), user_id=user1.id)
    post3 = Post(title="Third Post", content="Content for third post", created_at=datetime.now(), user_id=user2.id)
    post4 = Post(title="Fourth Post", content="Content for fourth post", created_at=datetime.now(), user_id=user2.id)
    post5 = Post(title="Fifth Post", content="Content for fifth post", created_at=datetime.now(), user_id=user3.id)
    post6 = Post(title="Sixth Post", content="Content for sixth post", created_at=datetime.now(), user_id=user3.id)
    post7 = Post(title="Seventh Post", content="Content for seventh post", created_at=datetime.now(), user_id=user4.id)
    post8 = Post(title="Eighth Post", content="Content for eighth post", created_at=datetime.now(), user_id=user4.id)
    post9 = Post(title="Ninth Post", content="Content for ninth post", created_at=datetime.now(), user_id=user5.id)
    post10 = Post(title="Tenth Post", content="Content for tenth post", created_at=datetime.now(), user_id=user5.id)
    # Add more posts to make a total of 10

    db.session.add_all([post1, post2, post3, post4, post5, post6, post7, post8, post9, post10])
    db.session.commit()

    # Create tags
    tag1 = Tag(name="Python")
    tag2 = Tag(name="Flask")
    tag3 = Tag(name="SQLAlchemy")

    db.session.add_all([tag1, tag2, tag3])
    db.session.commit()

    # Associate tags with posts
    post1.tags.append(tag1)
    post2.tags.append(tag2)
    post3.tags.append(tag3)
    post4.tags.append(tag1)
    post5.tags.append(tag2)

    db.session.commit()

print("Seed data created successfully.")
