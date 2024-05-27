from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(_name_)

Database connection detailsDB_HOST = 'your_mariadb_host'DB_USER = 'your_username'DB_PASSWORD = 'your_password'DB_NAME = 'blog_db'

Function to create a database connectiondef create_connection():    connection = None    try:        connection = mysql.connector.connect(            host=DB_HOST,            user=DB_USER,            password=DB_PASSWORD,            database=DB_NAME        )    except Error as e:        print(f"The error '{e}' occurred")    return connection

@app.route('/submit', methods=['POST'])
def submit_post():
title = request.form['title']
content = request.form['content']
author = request.form['author']

Create a connection    connection = create_connection()    cursor = connection.cursor()

Insert the data into the database    query = """    INSERT INTO posts (title, content, author)     VALUES (%s, %s, %s)    """    values = (title, content, author)    cursor.execute(query, values)    connection.commit()

Close the connection    cursor.close()    connection.close()

Return a JSON response    return jsonify({        'title': title,        'content': content,        'author': author    })

@app.route('/posts', methods=['GET'])
def get_posts():
connection = create_connection()
cursor = connection.cursor(dictionary=True)
cursor.execute("SELECT title, content, author, timestamp FROM posts ORDER BY timestamp DESC")
posts = cursor.fetchall()

cursor.close()
connection.close()

return jsonify(posts)

if _name_ == '_main_':
app.run(debug=True)
