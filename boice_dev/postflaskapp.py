from flask import Flask, render_template, request

app = Flask(__name__)

# In-memory storage for posts (replace with a database in production)
posts = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        post = request.form.get('post')
        posts.append((username, post))
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)