from datetime import datetime
from flaskblog import db

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(150), unique=True, nullable=False)
    image_file=db.Column(db.String(20),default='default.jpg', nullable=False)
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Post', backref='author', lazy=True)
    
    def __repr__(self):
        return f"user('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), unique=True, nullable=False)
    dateposted=db.Column(db.DateTime, nullable=False, default=datetime.now)
    content=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.String(20), db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"user('{self.title}','{self.dateposted}')"
