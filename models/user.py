from . import db
from flask_login import UserMixin
from .follower_db import follow_info
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    tweets = db.relationship('Tweet', backref='user', lazy=True)

    following = db.relationship(
        'User',
        secondary=follow_info,
        primaryjoin=(follow_info.c.follower_id == id),
        secondaryjoin=(follow_info.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic',
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, password, email):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
