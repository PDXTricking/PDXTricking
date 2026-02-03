from flask_login import login_user, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from flask import current_app
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from sqlalchemy.exc import IntegrityError
from models import db, User

def _get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

def generate_password_reset_token(email, expires_sec=3600):
    user = User.query.filter_by(email=email).first()
    if not user:
        return None
    s = _get_serializer()
    return s.dumps({'user_id': user.id}, salt='password-reset-salt')

def verify_password_reset_token(token, max_age=3600):
    s = _get_serializer()
    try:
        data = s.loads(token, salt='password-reset-salt', max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None
    return User.query.get(data.get('user_id'))

def set_password(user, new_password):
    user.password_hash = generate_password_hash(new_password).decode('utf-8')
    db.session.commit()

def register_user(username, email, password):
    hashed_password = generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False
    return True

def login_user_func(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return True
    return False

def logout_user_func():
    logout_user()