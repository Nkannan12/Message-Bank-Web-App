from flask import Flask, g, render_template, request
import sqlite3
import os

app = Flask(__name__)

def get_message_db():
    try:
        return g.message_db #check to see if the database exists
    except:
        g.message_db = sqlite3.connect("message_db.sqlite") #create database if doesn't exist
        cmd = \
        """
        CREATE TABLE IF NOT EXISTS messages (
            handle TEXT, 
            message TEXT
        )
        """
        with g.message_db:
            cursor = g.message_db.cursor() 
            cursor.execute(cmd) #creates a table called messages with columns handle and message
        return g.message_db
    
def insert_message(request):
    handle = request.form["name"] #extract handle
    message = request.form["message"] #extract message

    db = get_message_db() #work with database using method from aboe
    cmd = \
    """
    INSERT INTO messages (handle, message) VALUES (?, ?)
    """
    with db:
        cursor = db.cursor()
        cursor.execute(cmd, (handle, message)) #execute cmd, inserting message and handl into table (parametrized)
        db.commit()

def random_messages(n):
    db = get_message_db()
    cmd = \
    """
    SELECT * FROM messages ORDER BY RANDOM() LIMIT ?
    """
    with db:
        cursor = db.cursor()
        cursor.execute(cmd, (n,))
        selected_messages = cursor.fetchall() #fethces all responses for future display
        return selected_messages
    
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html', thanks=False)
    else:
        insert_message(request)
        return render_template('submit.html', thanks=True) #makes sure to post response

@app.route('/view/')
def view():
    messages = random_messages(5) #caps the number of messages shown at 5
    return render_template('view.html', messages=messages)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))