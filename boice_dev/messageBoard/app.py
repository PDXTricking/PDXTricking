#imports
import os
from io import BytesIO
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

#flask imports
from flask import Flask, request, render_template, send_file, redirect, url_for
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#mysql imports
import mysql.connector
from mysql.connector import Error

#Our imports
from message_board import get_all_posts, submit_a_post, delete_all_posts, delete_all_battles


load_dotenv(dotenv_path='/var/www/pdxflaskapp/pdxflaskapp/.env')

app = Flask(__name__)

# Database connection details
DB_HOST = '127.0.0.1'
DB_USER = os.getenv('BLOG_DB_USER')
DB_PASSWORD = os.getenv('BLOG_DB_PW')

#Blog DB
BLOG_DB_NAME = 'blog_db'

# File Share DB
FS_DB_NAME = 'fs_db'
BT_DB_NAME = 'bt_db'
DB_CONNECTOR= 'mysql+mysqlconnector'

# Configure the first database (SQLite)
app.config['SQLALCHEMY_BINDS'] = {
    'fs_db': "{}://{}:{}@{}/{}".format(DB_CONNECTOR,DB_USER,DB_PASSWORD,DB_HOST,FS_DB_NAME),
    'bt_db': "{}://{}:{}@{}/{}".format(DB_CONNECTOR,DB_USER,DB_PASSWORD,DB_HOST,BT_DB_NAME)
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure the upload folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
#if not os.path.exists(UPLOAD_FOLDER):
#    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

#fileshare db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model for storing user information in the first database
class User(db.Model):
    __bind_key__ = 'bt_db'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    photo_filename = db.Column(db.String(120), nullable=False)
    votes = db.Column(db.Integer, default=0)
    battle = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.name}>'

class File(db.Model):
    __bind_key__ = 'fs_db'
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)


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
            database=BLOG_DB_NAME
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Function to check if the uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

#### START Battle Vote Submission ####
# Route for the battle submission page
@app.route('/submitbattle')
def submitbattle():
    # Fetch all users from both databases
    users = User.query.all()
    return render_template('submitbattle.html', users=users)

# Route for battle view page
@app.route('/battle')
def battle():
    # Query users sorted by 'battle' value
    users = User.query.order_by(User.battle).all()

    # Group users by 'battle' value
    grouped_users = {}
    for user in users:
        if user.battle not in grouped_users:
            grouped_users[user.battle] = []
        grouped_users[user.battle].append(user)

    return render_template('battle.html', grouped_users=grouped_users)

# Route for handling file uploads and name submission
@app.route('/uploadbattle', methods=['POST'])
def upload_battle_file():
    if 'name' not in request.form or 'file' not in request.files:
        return "Form data or file missing", 400

    name = request.form['name']
    battle = request.form['battle']
    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Save to the database
        new_user = User(name=name, battle=battle, photo_filename=filename)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('submitbattle'))

    return "Invalid file type", 400

# Route for voting
@app.route('/vote/<int:user_id>', methods=['POST'])
def vote(user_id):

    user = User.query.get(user_id)
    if user:
        user.votes += 1
        db.session.commit()

    return redirect(url_for('battle'))

# Route for delete battles
@app.route('/delete_battle', methods=['POST'])
def delete_battle():
    return delete_all_battles(db, User)

#### END Battle Vote Submission ####

#########################-START FILE SHARE-###########################################
@app.route('/uploadfile', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    new_file = File(filename=file.filename, data=file.read())
    db.session.add(new_file)
    db.session.commit()
    return redirect(url_for('file_share_page'))

@app.route('/download/<int:file_id>')
def download(file_id):
    file_data = File.query.get(file_id)
    if file_data:
        return send_file(BytesIO(file_data.data), download_name=file_data.filename, as_attachment=True)
    return 'File not found'

@app.route('/fileShare')
def file_share_page():
    files = File.query.with_entities(File.id, File.filename).all()
    return render_template('fileShare.html', files=files)

######################-END FILE SHARE-################################

@app.route('/submit', methods=['POST'])
def submit_post():
    connection = create_connection()
    submit_a_post(connection)
    connection.close()

@app.route('/posts', methods=['GET'])
@cross_origin(origins=['https://www.pdxtricking.org'], methods=['GET'], allow_headers=['Content-Type'])
def get_posts():
    connection = create_connection()
    return get_all_posts(connection)

# Function to delete expired posts
@app.route('/deleteposts', methods=['POST'])
def delete_expired_posts():
    connection = create_connection()
    delete_all_posts(connection)

    connection.close()

#######################- Routes -################################
@app.route('/delete')
def delete_page():
    return render_template('delete.html')

@app.route('/message')
def message_board():
    return render_template('messageboard.html')

if __name__ == '__main__':
    # Create the database tables if they don't exist

    app.run()