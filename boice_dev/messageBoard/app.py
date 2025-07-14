# imports
import os
from io import BytesIO
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import pandas as pd
import io

# flask imports
from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user
from flask_bcrypt import Bcrypt

# mysql imports
import mysql.connector
from mysql.connector import Error

# Our imports
from message_board import get_all_posts, submit_a_post, delete_all_posts, delete_all_battles
from user_management import register_user, login_user_func, logout_user_func
from models import db, create_user_table

load_dotenv(dotenv_path='/var/www/pdxflaskapp/pdxflaskapp/.env')

app = Flask(__name__)

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
create_user_table(app)  # Create the User table

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

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
@login_required
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run()
