from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_user_table(app):
    with app.app_context():
        class User(UserMixin, db.Model):
            __tablename__ = 'user'
            __bind_key__ = 'user_db'
            __table_args__ = {'extend_existing': True}
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(64), unique=True, nullable=False)
            email = db.Column(db.String(128), unique=True, nullable=False)
            password_hash = db.Column(db.String(128), nullable=False)
            created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

        db.create_all()  # Remove the 'bind' argument
        return User
