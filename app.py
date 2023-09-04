
from flask import Flask, render_template, redirect, request, session, Response, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from voice_assistant import ChatBot, conversation  # Import the conversation variable from voice_assistant.py
from utils import calculate_stress_level, calculate_emotion_percentages
from models import db, User, StressLevel
import os
import json
import time
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

def create_app():
    app = Flask(__name__)

    # Configure the database URI (Change this to your desired database URI)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/malithg/PycharmProjects/pythonProject/New_Voice_Assistant/database/database1.db'
    app.config['SECRET_KEY'] = os.urandom(24)

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Initialize the LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'login'  # Set the login view name
    login_manager.init_app(app)

    # Create an instance of ChatBot
    ai = ChatBot(name="AIC")

    # Define the user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    def index():
        if "user_id" in session:
            user = User.query.get(session["user_id"])
            conversation = []  # Initialize an empty conversation list
            return render_template("index.html", emotion_percentages={}, conversation=conversation, user=user)
        return redirect("/login")

    @app.route("/sse_conversation_updates")
    def sse_conversation_updates():
        def generate_sse_updates():
            last_event_id = 0
            while True:
                if len(conversation) > last_event_id:
                    for i in range(last_event_id, len(conversation)):
                        message = conversation[i]
                        print("Sending SSE:", message)  # Add this line for debugging
                        yield f"data: {json.dumps(message)}\n\n"
                    last_event_id = len(conversation)
                time.sleep(1)  # Add a delay to avoid high server load

        return Response(generate_sse_updates(), content_type="text/event-stream")

    @app.route("/process_route")
    def process_route():
        user = User.query.get(session["user_id"])
        ai.run()  # Run the AI counselor logic

        # Calculate stress level based on emotions detected
        stress_level = calculate_stress_level(ai.sentiment_analysis)

        # Update the user's stress level in the database
        user.stress_level = stress_level
        db.session.commit()

        emotion_percentages = calculate_emotion_percentages(ai.sentiment_analysis)

        # Return a JSON response with emotion percentages

        response_data = {
            "stress_level": stress_level,
            "emotion_percentages": emotion_percentages
        }


        return jsonify(response_data)

    @app.route("/process")
    def process():
        if "user_id" not in session:
            return redirect("/login")

        return render_template("index.html", emotion_percentages={})

    @app.route("/reset", methods=["POST"])
    def reset():
        ai.sentiment_analysis = []  # Clear the emotions list
        sentiment_analysis = ai.sentiment_analysis
        emotion_percentages = calculate_emotion_percentages(sentiment_analysis)
        return jsonify(emotion_percentages)

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

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
