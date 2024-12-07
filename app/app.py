from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'weapon'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

def get_db_connection():
    return sqlite3.connect('../GameDB.sqlite')

@app.route('/')
def home():
    return "Welcome to the Flask App!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
    #         session['admin'] = True
    #         return redirect(url_for('admin_page'))
    #     else:
    #         return '<h1>Invalid credentials</h1>'
    return render_template('login.html')

@app.route('/portal')
def admin_page():
    # if not session.get('admin'):
    #     return redirect(url_for('login'))
    return render_template('portal.html')


@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/read')
def read_page():
    # conn = get_db_connection()
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM Player")
    # players = cursor.fetchall()
    # conn.close()
    return render_template('read.html')

@app.route('/create')
def create_page():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     gender = request.form['gender']
    #     conn = get_db_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("INSERT INTO Player (Username, Gender) VALUES (?, ?)", (username, gender))
    #     conn.commit()
    #     conn.close()
    #     return redirect(url_for('read'))
    return render_template('create.html')

@app.route('/delete')
def delete_page():
    # conn = get_db_connection()
    # cursor = conn.cursor()
    # cursor.execute("DELETE FROM Player WHERE EntityID = ?", (player_id,))
    # conn.commit()
    # conn.close()
    return redirect(url_for('delete.html'))

@app.route('/update')
def update_page():
    return render_template('update.html')

if __name__ == '__main__':
    app.run(debug=True)
