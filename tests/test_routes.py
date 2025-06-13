# tests/test_routes.py
import pytest
import os
from dotenv import load_dotenv
from app import create_app, db

# Load environment variables from .env file if it exists
load_dotenv()


@pytest.fixture(scope="function")
def flask_client():
    """Configures the Flask app for testing and sets up an in-memory database for routes testing."""
    # Create a test app instance
    app = create_app(
        {
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "TESTING": True,
            "SECRET_KEY": os.getenv("SECRET_KEY") or os.urandom(24).hex(),
        }
    )

    with app.app_context():
        db.create_all()

    testing_client = app.test_client()

    yield testing_client

    with app.app_context():
        db.drop_all()


def test_index_page(flask_client):
    """Tests that the index page loads successfully."""
    response = flask_client.get("/")
    assert response.status_code == 200
    assert b"Welcome to Todo App" in response.data


def test_register_login_flow(flask_client):
    """Tests the user registration, logout, and login process."""
    # Test registration
    response = flask_client.post(
        "/register",
        data={"username": "newuser", "password": "newpassword"},
        follow_redirects=True,
    )
    assert (
        b"Hello, newuser! Your Tasks" in response.data
    )  # Check if dashboard shows username and tasks

    # Test logout
    response = flask_client.get("/logout", follow_redirects=True)
    assert b"Login" in response.data  # Back to login page

    # Test login
    response = flask_client.post(
        "/login",
        data={"username": "newuser", "password": "newpassword"},
        follow_redirects=True,
    )
    assert b"Your Tasks" in response.data  # Check if dashboard content is present


def test_add_task_with_priority(flask_client):
    """Tests adding a task with a priority and verifies its display on the dashboard."""
    # First, register and log in a user
    flask_client.post(
        "/register",
        data={"username": "testuser_priority", "password": "testpassword"},
        follow_redirects=True,
    )
    response = flask_client.post(
        "/login",
        data={"username": "testuser_priority", "password": "testpassword"},
        follow_redirects=True,
    )
    assert b"Your Tasks" in response.data

    # Add a task with priority
    response = flask_client.post(
        "/add_task",
        data={
            "description": "Buy milk with priority",
            "due_date": "",
            "priority": "High",
        },
        follow_redirects=True,
    )
    assert b"Buy milk with priority" in response.data
    assert b"High" in response.data  # Assert that High priority is displayed

    # Test logout
    response = flask_client.get("/logout", follow_redirects=True)
    assert b"Login" in response.data
