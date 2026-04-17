import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'lucas_music_key_2026'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    if 'notes' not in session:
        session['notes'] = []
    if 'items' not in session:
        session['items'] = []
    return render_template('home.html', notes=session['notes'])

@app.route('/add_note', methods=['POST'])
def add_note():
    note = request.form.get('noteText')
    if note:
        notes = session.get('notes', [])
        notes.append(note)
        session['notes'] = notes
        session.modified = True
    return redirect(url_for('home'))

@app.route('/items')
def items():
    return render_template('items.html', items=session.get('items', []))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        artist = request.form.get('artist')
        album = request.form.get('album')
        genre = request.form.get('genre')
        rating = request.form.get('rating')
        review = request.form.get('review')
        file = request.files.get('albumCover')

        if not title or not rating:
            return redirect(url_for('add'))

        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_item = {
            'title': title,
            'artist': artist,
            'album': album,
            'genre': genre,
            'rating': rating,
            'review': review,
            'cover': filename
        }

        items_list = session.get('items', [])
        items_list.append(new_item)
        session['items'] = items_list
        session.modified = True
        return redirect(url_for('items'))
    return render_template('add.html')

@app.route('/remove')
def remove():
    return render_template('remove.html', items=session.get('items', []))

@app.route('/delete/<int:index>')
def delete_item(index):
    items_list = session.get('items', [])
    if 0 <= index < len(items_list):
        items_list.pop(index)
        session['items'] = items_list
        session.modified = True
    return redirect(url_for('remove'))

@app.route('/fun')
def fun():
    return render_template('fun.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5000, debug=True)