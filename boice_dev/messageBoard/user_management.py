from flask_login import login_user, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from models import db, User

def register_user(username, email, password):
    hashed_password = generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

def login_user_func(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return True
    return False

def logout_user_func():
    logout_user()