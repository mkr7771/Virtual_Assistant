from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user'  # Specify the existing table name
    __table_args__ = {'extend_existing': True}  # Add this line

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_active(self):
        return True  # You can customize this logic based on your application's requirements

class StressLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stress_level = db.Column(db.String(255), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('stress_levels', lazy=True))

    def __init__(self, user_id, stress_level):
        self.user_id = user_id
        self.stress_level = stress_level
