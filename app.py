"""Blogly application."""

from flask import Flask, render_template, redirect, url_for, request, flash, redirect
from models import db, connect_db, User, Post, Tag
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '123456789'

connect_db(app)
db.create_all()
app.app_context().push()

migrate = Migrate(app, db)

@app.route('/home')
def home_redirect():
    return redirect(url_for('show_recent_posts'))

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
    tags = Tag.query.all()

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        tag_ids = request.form.getlist('tags')
        new_tag_name = request.form.get('new_tag', '').strip()

        if not title or not content:
            flash('Title and content are required!', 'error')
            return redirect(url_for('new_post', user_id=user_id))

        new_post = Post(title=title, content=content, user_id=user.id)

        if new_tag_name:
            existing_tag = Tag.query.filter_by(name=new_tag_name).first()
            if not existing_tag:
                new_tag = Tag(name=new_tag_name)
                db.session.add(new_tag)
                db.session.commit()
                tag_ids.append(new_tag.id) 

        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag:
                new_post.tags.append(tag)

        db.session.add(new_post)
        db.session.commit()

        flash('Post created successfully!', 'success')
        return redirect(url_for('show_user', user_id=user.id))

    return render_template('posts/new.html', user=user, tags=tags)


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post and its details."""
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    user = post.user
    return render_template('posts/detail.html', post=post, user=user, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """Show form to edit a post or handle editing of the post."""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']

        new_tag_name = request.form.get('new_tag')
        if new_tag_name:

            existing_tag = Tag.query.filter_by(name=new_tag_name).first()
            if not existing_tag:
                new_tag = Tag(name=new_tag_name)
                db.session.add(new_tag)
                db.session.commit()
                tags.append(new_tag)

        selected_tag_ids = request.form.getlist('tags')
        post.tags = []

        for tag_id in selected_tag_ids:
            tag = Tag.query.get(tag_id)
            if tag:
                post.tags.append(tag)

        if not post.title or not post.content:
            flash('Title and content are required!', 'error')
            return redirect(url_for('edit_post', post_id=post_id))
        
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('show_post', post_id=post.id))
    
    return render_template('posts/edit.html', post=post, tags=tags)



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
    for post in posts:
        db.session.refresh(post)
    return render_template('home.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/tags')
def list_tags():
    """Show a list of all tags."""
    tags = Tag.query.all()
    return render_template('tags/list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def posts_by_tag(tag_id):
    """Show posts associated with a specific tag."""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template('tags/posts_by_tag.html', tag=tag, posts=posts)


@app.route('/tags/new', methods=["GET", "POST"])
def add_tag():
    """Add a new tag."""
    if request.method == "POST":
        name = request.form['name']
        if Tag.query.filter_by(name=name).first():
            flash('Tag name must be unique', 'error')
            return redirect(url_for('add_tag'))
        
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        flash('Tag created!', 'success')
        return redirect(url_for('list_tags'))

    return render_template('tags/new.html')