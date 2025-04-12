
from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

users = {
    'admin': {'username': 'admin', 'email': 'admin@example.com', 'password': 'admin', 'blocked': []}
}

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if username in users:
            return 'User already exists'
        users[username] = {'username': username, 'email': email, 'password': password, 'blocked': []}
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/settings', methods=['GET'])
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user = users[username]
    blocked_users = user['blocked']
    return render_template('settings.html', user=user, blocked_users=blocked_users)

@app.route('/unblock', methods=['POST'])
def unblock():
    username = session['username']
    unblock_user = request.form['username']
    users[username]['blocked'].remove(unblock_user)
    return redirect(url_for('settings'))

if __name__ == '__main__':
    app.run(debug=True)
