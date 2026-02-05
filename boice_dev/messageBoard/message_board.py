#imports
from flask import request, jsonify, redirect, url_for
from datetime import datetime, timedelta

def get_all_posts(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT title, content, author, timestamp FROM posts ORDER BY timestamp DESC")
    posts = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(posts)

def submit_a_post(connection):
    title = request.form['title']
    content = request.form['content']
    author = request.form['author']
    expiration_time = datetime.now() + timedelta(days=7)

    # Create a connection
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

    # Return a JSON response
    return jsonify({
        'title': title,
        'content': content,
        'author': author,
        'expiration_time': expiration_time.strftime('%Y-%m-%d %H:%M:%S')
    })

def delete_all_posts(connection):
    cursor = connection.cursor()

    # Delete expired posts
    query = "DELETE FROM posts WHERE expiration_time <= NOW()"
    cursor.execute(query)
    connection.commit()
    cursor.close()

def delete_all_battles(db, User):
    try:
        # Delete all records from the User table
        db.session.query(User).delete()
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        return str(e), 500