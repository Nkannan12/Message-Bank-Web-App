'''
At the command line, run 

conda activate PIC16B-24W
export FLASK_ENV=development
flask run
'''
from flask import Flask, g, render_template, request
import sqlite3
import os

app = Flask(__name__)

def get_message_db():
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("message_db.sqlite")
        cmd = \
        """
        CREATE TABLE IF NOT EXISTS messages (
            handle TEXT,
            message TEXT
        )
        """
        with g.message_db:
            cursor = g.message_db.cursor()
            cursor.execute(cmd)
        return g.message_db
    
def insert_message(request):
    handle = request.form["name"]
    message = request.form["message"]

    db = get_message_db()
    cmd = \
    """
    INSERT INTO messages (handle, message) VALUES (?, ?)
    """
    with db:
        cursor = db.cursor()
        cursor.execute(cmd, (handle, message))
        db.commit()
        db.close()

def random_messages(n):
    db = get_message_db()
    cmd = \
    """
    SELECT * FROM messages ORDER BY RANDOM() LIMIT ?
    """
    with db:
        cursor = db.cursor()
        cursor.execute(cmd, (n,))
        selected_messages = cursor.fetchall()
        db.close()
        return selected_messages
    
@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html', thanks=False)
    else:
        insert_message(request)
        return render_template('submit.html', thanks=True)

@app.route('/view')
def view():
    messages = random_messages(5)
    return render_template('view.html', messages=messages)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))