To display all posts from the database on the HTML page, you'll need to:

1. Update the HTML page to include a section for displaying the posts.
2. Create a new route in the Flask app to fetch the posts from the database.
3. Use JavaScript to fetch and display the posts dynamically.

Here’s how you can do it:





Updated HTML Page

Add a section to display the posts and JavaScript to fetch them from the Flask app.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog Post Submission</title>
</head>
<body>
<h1>Write a Blog Post</h1>
<form id="blogForm">
<label for="title">Title:</label><br>
<input type="text" id="title" name="title" required><br><br>

<label for="content">Content:</label><br>
<textarea id="content" name="content" rows="10" cols="50" required></textarea><br><br>

<label for="author">Your Name:</label><br>
<input type="text" id="author" name="author" required><br><br>

<input type="submit" value="Submit">
</form>

<h2>All Posts</h2>
<div id="posts">
<!-- Posts will be dynamically inserted here -->
</div>

<script>
document.getElementById('blogForm').addEventListener('submit', function(event) {
event.preventDefault(); // Prevent the default form submission

const title = document.getElementById('title').value;
const content = document.getElementById('content').value;
const author = document.getElementById('author').value;

const xhr = new XMLHttpRequest();
xhr.open('POST', '/submit', true);
xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

xhr.onreadystatechange = function () {
if (xhr.readyState === 4 && xhr.status === 200) {
const response = JSON.parse(xhr.responseText);
alert(`Blog post submitted successfully!\nTitle: ${response.title}\nContent: ${response.content}\nAuthor: ${response.author}`);
fetchPosts(); // Refresh the posts
}
};

const params = `title=${encodeURIComponent(title)}&content=${encodeURIComponent(content)}&author=${encodeURIComponent(author)}`;
xhr.send(params);
});

function fetchPosts() {
const xhr = new XMLHttpRequest();
xhr.open('GET', '/posts', true);

xhr.onreadystatechange = function () {
if (xhr.readyState === 4 && xhr.status === 200) {
const posts = JSON.parse(xhr.responseText);
const postsContainer = document.getElementById('posts');
postsContainer.innerHTML = ''; // Clear current posts
posts.forEach(post => {
const postElement = document.createElement('div');
postElement.innerHTML = `
<h3>${post.title}</h3>
<p>${post.content}</p>
<p><strong>Author:</strong> ${post.author}</p>
<p><em>${post.timestamp}</em></p>
<hr>
`;
postsContainer.appendChild(postElement);
});
}
};

xhr.send();
}

// Fetch posts when the page loads
document.addEventListener('DOMContentLoaded', fetchPosts);
</script>
</body>
</html>
```





Updated Flask App

Add a new route to fetch all posts from the database.

```python
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
```





Explanation

1. *New Route `/posts`*: This route fetches all posts from the database and returns them as a JSON array.
2. *Fetching Posts on Page Load*: JavaScript fetches posts from the `/posts` route and dynamically inserts them into the HTML.
3. *Updating Posts*: After a new post is submitted, the list of posts is refreshed to include the new post.





Running the Flask App

1. Save the updated Flask app code in `app.py`.

2. Ensure the `index.html` file is in the `templates` directory.
3. Install Flask and `mysql-connector-python` if you haven't already:

```bash
pip install flask mysql-connector-python
```

4. Run the Flask app:

```bash
python app.py
```

5. Open a web browser and go to `http://127.0.0.1:5000/submit`.

6. Fill out the form and submit it. The page will display all posts from the MariaDB database, including the newly submitted one.
