"""Blogly application."""

from flask import Flask, render_template, redirect, url_for, request, flash, redirect
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

# @app.route('/')
# def home_redirect():
#     """Redirect to the list of users."""
#     return redirect(url_for('list_users'))

@app.route('/users')
def list_users():
    """Show a list of all users."""
    users = User.query.all()
    return render_template('users/list.html', users=users)

@app.route('/users/new', methods=["GET", "POST"])
def add_user():
    """Show a form to add a new user or process form submission."""
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url'] or None

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('list_users'))
    
    return render_template('users/new.html')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user."""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('users/detail.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """Show a form to edit a user or process the edit form."""
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']

        db.session.commit()

        return redirect(url_for('show_user', user_id=user.id))

    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('list_users'))

@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def new_post(user_id):
    """Show form to add a post for that user or handle post submission."""
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']

        if not title or not content:
            flash('Title and content are required!', 'error')
            return redirect(url_for('show_new_post_form', user_id=user_id))

        new_post = Post(title=title, content=content, user_id=user.id)
        db.session.add(new_post)
        db.session.commit()

        flash('Post created successfully!', 'success')
        return redirect(url_for('show_user', user_id=user.id))
    
    return render_template('posts/new.html', user=user)

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post and its details."""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/detail.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """Show form to edit a post or handle editing of the post."""
    post = Post.query.get_or_404(post_id)

    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']

        if not post.title or not post.content:
            flash('Title and content are required!', 'error')
            return redirect(url_for('show_edit_post_form', post_id=post_id))
        
        db.session.commit()

        return redirect(url_for('show_post', post_id=post.id))
    
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete a post."""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('show_user', user_id=user_id))

@app.route('/')
def show_recent_posts():
    """Show the 5 most recent posts."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404