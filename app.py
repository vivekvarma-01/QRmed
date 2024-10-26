from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import qrcode
import bcrypt
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For session management

# MongoDB setup
client = MongoClient('//Copy the mongodb database url form mongodb atlas Here')
db = client['health']
users_collection = db['users']

# Home route - Login page
@app.route('/')
def index():
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Validate email
        if '@' not in email or '.' not in email:
            return "Invalid email format, please try again."

        # Check if user already exists
        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            return "User already exists, please log in."

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user
        users_collection.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password,
            'profile': None,  # Profile details to be filled later
            'qr_code': None
        })
        return redirect(url_for('index'))
    
    return render_template('register.html')

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = users_collection.find_one({'username': username})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        session['username'] = username
        if user['profile']:
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('create_profile'))
    else:
        return "Invalid credentials or user does not exist."

# Create profile route for new users
@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        profile_data = {
            'name': request.form['name'],
            'age': request.form['age'],
            'blood_group': request.form['blood_group'],
            'emergency_contact': request.form['emergency_contact'],
            'medical_history': request.form['medical_history'],
            'blood_press': request.form['blood_press'],
            'sugar': request.form['sugar']
        }

        users_collection.update_one(
            {'username': session['username']},
            {'$set': {'profile': profile_data}}
        )
        
        # Generate QR code for user profile
        qr_code_data = f"http://(your locol host ip address for running the server)/view_profile/{session['username']}"
        qr = qrcode.make(qr_code_data)
        qr_path = f'static/{session["username"]}_qr.png'
        qr.save(qr_path)
        
        users_collection.update_one(
            {'username': session['username']},
            {'$set': {'qr_code': qr_path}}
        )
        return redirect(url_for('profile'))

    return render_template('create_profile.html')

# User profile page
@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('index'))

    user = users_collection.find_one({'username': session['username']})
    return render_template('profile.html', user=user)

# Edit profile route for existing users
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        updated_data = {
            'emergency_contact': request.form['emergency_contact'],
            'medical_history': request.form['medical_history'],
            'blood_press': request.form['blood_press'],
            'sugar': request.form['sugar']
        }

        users_collection.update_one(
            {'username': session['username']},
            {'$set': {'profile': updated_data}}
        )
        return redirect(url_for('profile'))

    user = users_collection.find_one({'username': session['username']})
    return render_template('edit_profile.html', user=user)

# Public profile view for QR code scans
@app.route('/view_profile/<username>')
def view_profile(username):
    user = users_collection.find_one({'username': username})
    if user and user['profile']:
        return render_template('view_profile.html', profile=user['profile'])
    else:
        return "Profile not found."

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,)
