from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy instance (this should be outside the create_app function)
db = SQLAlchemy()

# Function to initialize the core app
def create_app():
    app = Flask(__name__)

    # Configure app
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use SQLite for the database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

    # Initialize the database with the app
    db.init_app(app)

    # Import and register blueprints or routes
    from .views import main_bp
    app.register_blueprint(main_bp)

    return app

@app.route('/create-event', methods=['GET', 'POST'])
def create_event():
    if not is_logged_in():
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get form data
        home_team = request.form['home_team']
        away_team = request.form['away_team']
        venue = request.form['venue']
        event_date = request.form['event_date']
        event_time = request.form['event_time']
        description = request.form['description']
        seats_available = request.form['seats_available']
        
        # Handle image upload
        event_image = request.files['event_image']
        if event_image:
            filename = secure_filename(event_image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            event_image.save(filepath)
        
        # Save event to the database (you can integrate this into your DB model)
        flash('Event created successfully!', 'success')
        return redirect(url_for('show_events'))

    return render_template('create_event.html')

