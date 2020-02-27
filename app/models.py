from app import db, bcrypt
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Integer, default=1)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User({self.username}, {self.email}, role={self.role})"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    description = db.Column(db.String(500))
    thumbnail = db.Column(db.String(200), default='img/default.jpg')
    hide = db.Column(db.Integer, default=0)
    order_number = db.Column(db.Integer)
    overlay_title = db.Column(db.String(32))
    overlay_text = db.Column(db.String(32))
    link = db.Column(db.String(2083))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime)
