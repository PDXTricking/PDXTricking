from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

from werkzeug.utils import secure_filename
import magic, os

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_mime_type(file):
    mime = magic.from_buffer(file.stream.read(2048), mime=True)
    file.stream.seek(0)
    return mime in ['image/png', 'image/jpeg', 'image/gif']
