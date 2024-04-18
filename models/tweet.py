from . import db

likes = db.Table('likes',
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                 db.Column('tweet_id', db.Integer, db.ForeignKey('tweet.id')),
                 db.UniqueConstraint('user_id', 'tweet_id', name='unique_likes')
                 )


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    likes = db.relationship('User', secondary=likes, backref=db.backref('liked_tweets', lazy='dynamic'))

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return '<Tweet %r>' % self.content
