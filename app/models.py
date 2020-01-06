from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('密码是一个不可见的属性')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        if self.username == None:
            return '<用户id %r>' % self.id 
        
        return '<用户名 %r>' % self.username 