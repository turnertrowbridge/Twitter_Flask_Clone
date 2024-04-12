from . import db
from flask_login import UserMixin
from .follower_db import follow_info


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
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

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
