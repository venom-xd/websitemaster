from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from functools import wraps

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = os.urandom(24)  # Generate a random secret key for security

# Decorator to check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("You must be logged in to access this page.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Basic authentication check (use a more secure method in production)
        if username == 'admin' and password == 'password':  # Change these credentials
            session['username'] = username
            return redirect(url_for('admin_panel'))
        else:
            flash("Invalid credentials, please try again.", "danger")

    return render_template('login.html')

# Admin panel route
@app.route('/admin', methods=['GET', 'POST'])
@login_required  # Protect the admin panel route
def admin_panel():
    # Load internships from the text file
    internships = load_internships()
    
    if request.method == 'POST':
        if 'add' in request.form:
            name = request.form.get('name')
            info = request.form.get('info')
            link = request.form.get('link')
            add_internship(name, info, link)
            return redirect(url_for('admin_panel'))

    return render_template('admin_panel.html', internships=internships)

# Jobs route
@app.route('/jobs')
def jobs():
    # Load internships from the text file
    internships = load_internships()
    return render_template('jobs.html', internships=internships)

# Delete internship
@app.route('/delete/<int:index>')
@login_required  # Protect delete route
def delete_internship(index):
    internships = load_internships()
    if 0 <= index < len(internships):
        del internships[index]
        save_internships(internships)
    return redirect(url_for('admin_panel'))

# Logout route
@app.route('/logout')
@login_required  # Protect logout route
def logout():
    session.pop('username', None)  # Remove user from session
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

# Functions to manage internships
def load_internships():
    if not os.path.exists('internships.txt'):
        return []
    with open('internships.txt', 'r') as f:
        return [line.strip().split('|') for line in f.readlines()]

def save_internships(internships):
    with open('internships.txt', 'w') as f:
        for internship in internships:
            f.write('|'.join(internship) + '\n')

def add_internship(name, info, link):
    internships = load_internships()
    internships.append([name, info, link])
    save_internships(internships)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
