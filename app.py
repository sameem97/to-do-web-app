"""Todo web application with user authentication and task management."""

import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()


class User(UserMixin, db.Model):
    """User model for authentication and task management."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    tasks = db.relationship("Task", backref="user", lazy=True)

    def set_password(self, password):
        """Set the user's password hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the user's password against the stored hash."""
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    """Task model for storing user tasks."""

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    priority = db.Column(db.String(50), nullable=True)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)  # Initialize db with the app
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login."""
        return User.query.get(int(user_id))

    @app.route("/")
    def index():
        """Render home page or redirect to dashboard if logged in."""
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        """Handle user login with username and password."""
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for("dashboard"))
            flash("Invalid username or password", "error")
        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        """Handle user registration with username and password."""
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if User.query.filter_by(username=username).first():
                flash("Username already exists")
                return redirect(url_for("register"))

            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for("dashboard"))
        return render_template("register.html")

    @app.route("/dashboard")
    @login_required
    def dashboard():
        """Display user's tasks on the dashboard."""
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return render_template("dashboard.html", tasks=tasks)

    @app.route("/add_task", methods=["POST"])
    @login_required
    def add_task():
        """Add a new task with optional due date and priority."""
        description = request.form.get("description")
        due_date_str = request.form.get("due_date")
        priority = request.form.get("priority")

        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")

        task = Task(
            description=description,
            due_date=due_date,
            priority=priority,
            user_id=current_user.id,
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("dashboard"))

    @app.route("/toggle_task/<int:task_id>")
    @login_required
    def toggle_task(task_id):
        """Toggle task completion status."""
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            return redirect(url_for("dashboard"))

        task.completed = not task.completed
        db.session.commit()
        return redirect(url_for("dashboard"))

    @app.route("/delete_task/<int:task_id>")
    @login_required
    def delete_task(task_id):
        """Delete a task by ID."""
        task = Task.query.get_or_404(task_id)
        if task.user_id != current_user.id:
            return redirect(url_for("dashboard"))

        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("dashboard"))

    @app.route("/logout")
    @login_required
    def logout():
        """Log out the current user and redirect to home page."""
        logout_user()
        return redirect(url_for("index"))

    return app  # Only return the app instance since we use the global db


app = create_app()  # Create the app instance

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
