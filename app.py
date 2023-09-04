import json
import pyttsx3
from datetime import datetime
from flask import Flask, render_template, redirect, request, session, flash, url_for, jsonify, Response
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from voice_assistant import ChatBot, conversation
from utils import calculate_stress_level, calculate_emotion_percentages
from models import db, User, StressLevel
import os
from flask_login import LoginManager, login_user, logout_user, login_required
import time

# Load the ChatBot model once during application startup
ai = ChatBot(name="AI Counselor")

app = Flask(__name__)

# Configure the database URI (Change this to your desired database URI)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/malithg/PycharmProjects/pythonProject/New_Voice_Assistant/database/database1.db'
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize SQLAlchemy with the app
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'  # Set the login view name
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        # Get the user's previous stress levels from the database
        previous_stress_levels = StressLevel.query.filter_by(user_id=user.id).all()
        conversation = []  # Initialize an empty conversation list
        return render_template("index.html", emotion_percentages={}, user=user, stress_levels=previous_stress_levels)
    return redirect("/login")

@app.route("/stream")
def stream():
    def generate_messages():
        last_message_index = 0
        while True:
            # Check if there are new messages in the conversation list
            if last_message_index < len(conversation):
                # Send the new message as plain text
                new_message = conversation[last_message_index]
                yield f"data: {new_message}\n\n"
                last_message_index += 1
            else:
                # No new messages, send an empty message to keep the connection alive
                yield "data: \n\n"
            time.sleep(1)  # Adjust the sleep interval as needed

    return Response(generate_messages(), content_type="text/event-stream")

@app.route("/process_route")
def process_route():
    user = User.query.get(session["user_id"])
    ai.run()  # Run the AI counselor logic

    # Calculate stress level based on emotions detected
    stress_level1 = calculate_stress_level(ai.sentiment_analysis)

    # Create a new StressLevel record for the user
    new_stress_level_record = StressLevel(user_id=user.id, stress_level=str(stress_level1), login_time=datetime.utcnow())

    previous_stress_levels = StressLevel.query.filter_by(user_id=user.id).all()
    # Add the new record to the database
    db.session.add(new_stress_level_record)
    db.session.commit()

    emotion_percentages = calculate_emotion_percentages(ai.sentiment_analysis)

    response_data = {
        "stress_level": stress_level1,
        "emotion_percentages": emotion_percentages
    }

    return render_template("index.html", stress_level=stress_level1, emotion_percentages=emotion_percentages, user=user, conversation=conversation, stress_levels=previous_stress_levels)

@app.route("/reset", methods=["POST"])
def reset():
    user = User.query.get(session["user_id"])
    ai.sentiment_analysis = []  # Clear the emotions list

    # Clear the user's session
    session.clear()

    # Redirect to the login page after resetting
    return redirect("/login")

# Remove the previous return statement from the /reset route


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password using generate_password_hash
        hashed_password = generate_password_hash(password, method='sha256')

        # Create a new user with the hashed password
        new_user = User(username=username, password=hashed_password)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]  # Retrieve the username from the form
        password = request.form["password"]

        # Check if the username and password are correct (you can add your logic here)
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Successful login
            login_user(user)  # Set the user in the session
            session["user_id"] = user.id
            flash("Login successful.", "success")
            return redirect("/")  # Redirect to the 'index.html' page

        # Failed login
        flash("Wrong username or password. Please try again.", "error")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
