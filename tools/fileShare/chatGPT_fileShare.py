from flask import Flask, request, send_file, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)

@app.route('/')
def index():
    files = File.query.all()
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    new_file = File(filename=file.filename, data=file.read())
    db.session.add(new_file)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/download/<int:file_id>')
def download(file_id):
    file_data = File.query.get(file_id)
    if file_data:
        return send_file(BytesIO(file_data.data), attachment_filename=file_data.filename, as_attachment=True)
    return 'File not found'

if __name__ == '__main__':
    app.run(debug=True)
