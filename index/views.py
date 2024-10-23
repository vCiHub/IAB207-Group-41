from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from index import db  # Import the db instance from your app file
from index.models import User  # Import the User model

# Define the Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('homepage.html')

# Registration route
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists! Please choose a different username.', 'danger')
            return redirect(url_for('main.register'))

        # Hash the password and save the new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(first_name=first_name, last_name=last_name, dob=dob, email=email, username=username, password=hashed_password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

# Login route
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists
        user = User.query.filter_by(username=username).first()

        if not user:
            flash('User not found. Please register first.', 'danger')
            return redirect(url_for('main.register'))

        # Verify the password
        if not check_password_hash(user.password, password):
            flash('Incorrect password. Please try again.', 'danger')
            return redirect(url_for('main.login'))

        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(url_for('main.home'))

    return render_template('login.html')
