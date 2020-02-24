from datetime import datetime
from flaskd3 import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    #comments = db.relationship('Comment', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Graph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    """"graph = db.Column(db.pygal.Line(), unique = False, nullable=False)"""

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #add graph svg here
    #image_file = db.Column(db.String(20), nullable=True, default='default.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

"""class Commenting(db.Model):
    comments = db.Column(db.String(500), unique=False)
    timestamp = db.Column(db.String(12), primary_key=True)
    timestamp = db.Column(db.String(12), primary_key=True)
    author = db.Column(db.String(12), primary_key=True)
    date_posted = db.Column(db.String(12), unique=False )
    data = db.Column(db.String(12), unique=False)
    comment = db.Column(db.String(500), unique=False)
    title = db.Column(db.String(12), unique=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
"""

class FileContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    data = db.Column(db.String(999999999))
    
    def __rep__(self):
        return f"FileContent('{self.name}')"




