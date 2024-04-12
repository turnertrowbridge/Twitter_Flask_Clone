from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash

from models.user import User
from models.tweet import Tweet
from models import db
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    tweets = Tweet.query.all()

    # Sort Tweets by created at and fetch first 20 records
    tweets = Tweet.query.order_by(Tweet.created_at.desc()).limit(20).all()

    # Get all user's usernames
    usernames = [user.username for user in User.query.all()]
    return render_template('index.html', tweets=tweets, usernames=usernames)


@app.route('/register', methods=['POST'])
def register():
    existing_user = User.query.filter_by(username=request.form['username']).first()
    if existing_user:
        flash('The username already exists.')
        print('The username already exists.')
        return redirect(url_for('index'))

    # Create a new user
    new_user = User(
        username=request.form['username'],
        password=request.form['password'],
        email=request.form['email']
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(username=request.form['username']).first()
    if user:
        if user.check_password(request.form['password']):
            login_user(user)

    return redirect(url_for('index'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/tweet', methods=['POST'])
@login_required
def tweet():
    tweet = Tweet(content=request.form['content'], user_id=current_user.id)
    db.session.add(tweet)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete_tweet', methods=['POST'])
@login_required
def delete_tweet():
    tweet = Tweet.query.get(request.form['tweet_id'])
    if tweet and tweet.user_id == current_user.id:
        db.session.delete(tweet)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    num_followers = user.followers.count()
    num_following = user.following.count()
    return render_template('profile.html', current_user=current_user, user=user, num_followers=num_followers,
                           num_following=num_following, tweets=user.tweets)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash(f'User {username} does not exist.')
        return redirect(url_for('index'))

    current_user.following.append(user)
    db.session.commit()

    flash(f'Successfully followed {username}.')
    return redirect(url_for('user', username=user.username))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash(f'User {username} does not exist.')
        return redirect(url_for('index'))

    current_user.following.remove(user)
    db.session.commit()

    flash(f'Successfully unfollowed {username}.')
    return redirect(url_for('user', username=user.username))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)
    app.run()
