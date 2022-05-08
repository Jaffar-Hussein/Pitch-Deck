from datetime import datetime
from . import db


class User(db.Model):
    """
    The table for the User in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String,nullable=False,unique=True)
    email = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    profile = db.Column(db.String,nullable=False,default='default.jpeg')
    pitches = db.relationship('Post', backref='author', lazy=True)
    
    def __init__(self):
        return f"id: {self.id} , username: {self.username} "

        
class Pitch(db.Model):
    """
    The talbe for the Pitches

    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,nullable=False)
    content = db.Column(db.String,nullable=False)
    date_created = db.Column(db.Date,nullable=False,default=datetime.utc.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self):
        return f"id: {self.id} , title: {self.title}"
