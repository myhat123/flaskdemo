from flask_login import UserMiXin

class User(UserMiXin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
