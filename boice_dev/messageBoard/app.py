from flask import Flask, request, jsonify, render_template
import mysql.connector
import os
from mysql.connector import Error
from datetime import datetime, timedelta
from flask_cors import cross_origin
from dotenv import load_dotenv

load_dotenv(dotenv_path='/var/www/pdxflaskapp/pdxflaskapp/.env')

app = Flask(__name__)

# Database connection details
DB_HOST = '127.0.0.1'
DB_USER = os.getenv('BLOG_DB_USER')
DB_PASSWORD = os.getenv('BLOG_DB_PW')
DB_NAME = 'blog_db'

# Render Homepage
@app.route("/")
def index():
    return render_template('index.html')

# Function to create a database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

@app.route('/submit', methods=['POST'])
def submit_post():
    title = request.form['title']
    content = request.form['content']
    author = request.form['author']
    expiration_time = datetime.now() + timedelta(days=7)

    # Create a connection
    connection = create_connection()
    cursor = connection.cursor()

    # Insert the data into the database
    query = """
    INSERT INTO posts (title, content, author, expiration_time) 
    VALUES (%s, %s, %s, %s)
    """
    values = (title, content, author, expiration_time)
    cursor.execute(query, values)
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()

    # Return a JSON response
    return jsonify({
        'title': title,
        'content': content,
        'author': author,
        'expiration_time': expiration_time.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/posts', methods=['GET'])
@cross_origin(origins=['https://www.pdxtricking.org'], methods=['GET'], allow_headers=['Content-Type'])
def get_posts():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT title, content, author, timestamp FROM posts ORDER BY timestamp DESC")
    posts = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(posts)

# Function to delete expired posts
@app.route('/deleteposts', methods=['POST'])
def delete_expired_posts():
    connection = create_connection()
    cursor = connection.cursor()

    # Delete expired posts
    query = "DELETE FROM posts WHERE expiration_time <= NOW()"
    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()

@app.route('/delete')
def delete_page():
    return render_template('delete.html')

if __name__ == '__main__':
    app.run()

