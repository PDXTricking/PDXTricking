import os
from flask import request, redirect, url_for
from flask_login import current_user, login_required
from models import db, BattleSubmission
from werkzeug.utils import secure_filename

def submit_battle(app):
    if request.method == 'POST':
        # Get the uploaded photos
        photo1 = request.files['photo1']
        photo2 = request.files['photo2']
        photo3 = request.files['photo3']

        # Save the photos to a desired location
        photo_dir = 'static/battle_photos'
        os.makedirs(photo_dir, exist_ok=True)

        photo_paths = []
        for photo in [photo1, photo2, photo3]:
            if photo:
                filename = secure_filename(photo.filename)
                photo_path = os.path.join(photo_dir, filename)
                photo.save(photo_path)
                photo_paths.append(photo_path)

        # Create a new battle submission entry in the database
        submission = BattleSubmission(user_id=current_user.id, photo_paths=photo_paths)
        db.session.add(submission)
        db.session.commit()

        return redirect(url_for('battle'))

    return redirect(url_for('submit_battle'))
