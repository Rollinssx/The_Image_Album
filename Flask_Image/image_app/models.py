from image_app import db
from datetime import datetime
from flask_login import LoginManager, UserMixin
from image_app import login_manager



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    images = db.relationship('Image', back_populates='uploader', lazy=True)


    def __repr__(self):
        return f"{self.username}, {self.email}, {self.image_file}"


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    the_image = db.Column(db.String(120), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    uploader = db.relationship('User', back_populates='images')




