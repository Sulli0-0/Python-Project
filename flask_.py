from flask import Flask, render_template, request, redirect, session
import os 
import json

reviewRequests = []
app = Flask(__name__)
app.secret_key = 'secretKey'
DATAFILE = 'items.json'

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
    return render_template('home.html', requests=reviewRequests)

@app.route('/items')
def items():
    items = load_items()
    return render_template('items.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_item = {'title': request.form['title'],
            'artist': request.form['artist'],
            'album': request.form['album'],
            'genre': request.form['genre'],
            'rating': request.form['rating'],
            'review': request.form['review']}
        items_list = load_items()
        items_list.append(new_item)
        save_items(items_list)
        return redirect('/items')
    return render_template('add.html')

@app.route('/delete/<int:index>')
def delete(index):
    items = load_items()
    if index < len(items):
        items.pop(index)
        save_items(items)
    return redirect('/items')

@app.route('/fun')
def fun():
    return render_template('fun.html')

@app.route('/request', methods=['POST'])
def requestReview():
    newRequest = request.form.get('requestText')
    if newRequest:
        reviewRequests.append(newRequest)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)