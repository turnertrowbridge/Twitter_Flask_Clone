from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
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
    users = [user.username for user in User.query.all()]
    return render_template('index.html', tweets=tweets, users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
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


   
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)
    app.run()
   
