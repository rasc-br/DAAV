"""
models.py
- This file contains all models to support appSentinel
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    # id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    username = db.Column(db.String(45), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        
        if not username or not password:
            return None

        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(id=self.id, username=self.username)
