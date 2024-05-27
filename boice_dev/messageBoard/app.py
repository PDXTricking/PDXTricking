from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)

# Database connection details
DB_HOST = '127.0.0.1'
DB_USER = 'boice'
DB_PASSWORD = 'Callofduty8'
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

    # Create a connection
    connection = create_connection()
    cursor = connection.cursor()

    # Insert the data into the database
    query = """
    INSERT INTO posts (title, content, author) 
    VALUES (%s, %s, %s)
    """
    values = (title, content, author)
    cursor.execute(query, values)
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()

    # Return a JSON response
    return jsonify({
        'title': title,
        'content': content,
        'author': author
    })

@app.route('/posts', methods=['GET'])
def get_posts():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT title, content, author, timestamp FROM posts ORDER BY timestamp DESC")
    posts = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(posts)

if __name__ == '__main__':
    app.run()

