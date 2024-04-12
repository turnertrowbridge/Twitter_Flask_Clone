from . import db

follow_info = db.Table(
    'follow_info',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
    db.UniqueConstraint('follower_id', 'followed_id', name='unique_followers')
    )
