# imports
import os
from io import BytesIO
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import pandas as pd
import io
import threading

# flask imports
from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message

# mysql imports
import mysql.connector
from mysql.connector import Error

# Our imports
from message_board import get_all_posts, submit_a_post, delete_all_posts, delete_all_battles
from user_management import register_user, login_user_func, logout_user_func, generate_password_reset_token, verify_password_reset_token, set_password
from models import db, User, BattleSubmission
from battle_management import submit_battle

load_dotenv(dotenv_path='/var/www/pdxflaskapp/pdxflaskapp/.env')

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Set the secret key

# Mail configuration (use environment variables; defaults for local dev)
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER', 'localhost'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 1025)),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS', 'False') == 'True',
    MAIL_USE_SSL=os.getenv('MAIL_USE_SSL', 'False') == 'True',
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER', 'noreply@example.com')
) 

#Competition ID
COMP_ID = 9

# Database connection details
DB_HOST = '127.0.0.1'
DB_USER = os.getenv('BLOG_DB_USER')
DB_PASSWORD = os.getenv('BLOG_DB_PW')

# Login DB
USER_DB_NAME = 'user_db'

DB_CONNECTOR = 'mysql+mysqlconnector'

app.config['SQLALCHEMY_DATABASE_URI'] = "{}://{}:{}@{}/{}".format(DB_CONNECTOR, DB_USER, DB_PASSWORD, DB_HOST, USER_DB_NAME)
app.config['SQLALCHEMY_BINDS'] = {
    'user_db': "{}://{}:{}@{}/{}".format(DB_CONNECTOR, DB_USER, DB_PASSWORD, DB_HOST, USER_DB_NAME)
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

with app.app_context():
    db.create_all()  # Create all tables, including the battle_submission table

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
# Initialize Flask-Mail
mail = Mail(app)

# Send mail asynchronously in a background thread to avoid blocking requests
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg) 

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Function to create a database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=USER_DB_NAME
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Routes
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/battle')
def battle():
    submissions = BattleSubmission.query.filter_by(comp_id=COMP_ID).all()
    return render_template('battle.html', submissions=submissions)

@app.route('/submit_battle', methods=['GET'])
@login_required
def submit_battle_form():
    return render_template('submit_battle.html')

@app.route('/submit_battle', methods=['POST'])
@login_required
def submit_battle_route():
    return submit_battle(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if register_user(username, email, password):
            return redirect(url_for('login'))
        else:
            return "Registration failed"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user_func(username, password):
            return redirect(url_for('index'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user_func()
    return redirect(url_for('login'))

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        token = generate_password_reset_token(email)
        if token:
            reset_link = url_for('reset_with_token', token=token, _external=True)
            # Send the reset email (plain text + HTML). In dev, you can run a local SMTP server to inspect messages.
            msg = Message("Reset your password", recipients=[email])
            msg.body = f"To reset your password, visit: {reset_link}\nIf you didn't request this, ignore this email."
            msg.html = render_template('reset_email.html', reset_link=reset_link)
            try:
                thr = threading.Thread(target=send_async_email, args=(app, msg))
                thr.daemon = True
                thr.start()
            except Exception as e:
                # Fallback for dev environments where SMTP isn't configured
                print(f"Failed to send email: {e}. Reset link: {reset_link}")
        # Always return a generic response to avoid leaking whether the email exists
        return "If an account with that email exists, you'll receive an email with reset instructions."
    return render_template('reset_request.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    user = verify_password_reset_token(token)
    if not user:
        return "Invalid or expired token", 400
    if request.method == 'POST':
        password = request.form['password']
        set_password(user, password)
        return redirect(url_for('login'))
    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run()
