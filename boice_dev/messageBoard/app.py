#imports
import os
from io import BytesIO
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import pandas as pd
import io

#flask imports
from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#mysql imports
import mysql.connector
from mysql.connector import Error

#Our imports
from message_board import get_all_posts, submit_a_post, delete_all_posts, delete_all_battles
from userManagement import User, login_manager, bcrypt, register_user, login_user, logout_user

load_dotenv(dotenv_path='/var/www/pdxflaskapp/pdxflaskapp/.env')

app = Flask(__name__)

# Database connection details
DB_HOST = '127.0.0.1'
DB_USER = os.getenv('BLOG_DB_USER')
DB_PASSWORD = os.getenv('BLOG_DB_PW')

#Login DB
USER_DB_NAME = 'user_db'

DB_CONNECTOR= 'mysql+mysqlconnector'

# Configure the first database (SQLite)
""" Example
app.config['SQLALCHEMY_BINDS'] = {
    'fs_db': "{}://{}:{}@{}/{}".format(DB_CONNECTOR,DB_USER,DB_PASSWORD,DB_HOST,FS_DB_NAME),
    'bt_db': "{}://{}:{}@{}/{}".format(DB_CONNECTOR,DB_USER,DB_PASSWORD,DB_HOST,BT_DB_NAME)
} 
"""
app.config['SQLALCHEMY_BINDS'] = {
    'user_db': "{}://{}:{}@{}/{}".format(DB_CONNECTOR,DB_USER,DB_PASSWORD,DB_HOST,USER_DB_NAME)    
} 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


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


#######################- Routes -################################
# Render Homepage
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        register_user(username, email, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username, password):
            return redirect(url_for('index'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create the database tables if they don't exist

    app.run()