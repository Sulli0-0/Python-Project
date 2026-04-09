from flask import Flask, render_template, request, redirect, session
import os 
import json
from werkzeug.utils import secure_filename

userNotes = []
app = Flask(__name__)
app.secret_key = 'secretKey'
DATAFILE = 'items.json'

UPLOADFOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOADFOLDER
allowedExtensions = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOADFOLDER):
    os.makedirs(UPLOADFOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedExtensions

def load_items():
    if not os.path.exists(DATAFILE):
        return []
    with open(DATAFILE, 'r') as f:
        return json.load(f)
    
def save_items(items):
    with open(DATAFILE, 'w') as f:
        json.dump(items, f)

@app.route('/')
def home():
    return render_template('home.html', notes=userNotes)

@app.route('/items')
def items():
    items = load_items()
    return render_template('items.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        albumCover = request.files.get('albumCover')
        fileName = ""

        if albumCover and allowed_file(albumCover.filename):
            fileName = secure_filename(albumCover.filename)
            albumCover.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))    
        
        newItem = {'title': request.form['title'],
            'artist': request.form['artist'],
            'album': request.form['album'],
            'genre': request.form['genre'],
            'rating': request.form['rating'],
            'review': request.form['review'],
            'cover': fileName}
        itemsList = load_items()
        itemsList.append(newItem)
        save_items(itemsList)
        return redirect('/items')
    return render_template('add.html')

@app.route('/remove')
def remove():
    items = load_items()
    return render_template('remove.html', items=items)

@app.route('/delete/<int:index>')
def delete(index):
    items = load_items()
    if 0 <= index < len(items):
        items.pop(index)
        save_items(items)
    return redirect('/remove')

@app.route('/fun')
def fun():
    return render_template('fun.html')

@app.route('/note', methods=['POST'])
def addNote():
    newNote = request.form.get('noteText')
    if newNote:
        userNotes.append(newNote)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)