# tests/test_routes.py
import pytest
from app import app, db  # Assuming app.py


@pytest.fixture(scope="module")
def flask_client():
    """Configures the Flask app for testing and sets up an in-memory database for routes testing."""
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
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
    assert b"newuser" in response.data  # Check if dashboard shows username or similar

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
