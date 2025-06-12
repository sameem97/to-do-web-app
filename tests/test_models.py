# tests/test_models.py
import pytest
from app import app, db, User, Task  # Assuming your app.py is where these are defined


@pytest.fixture(scope="module")
def test_client():
    """Configures the Flask app for testing and sets up an in-memory database."""
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///:memory:"  # Use in-memory SQLite for tests
    )
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()  # Create tables for the in-memory database

    testing_client = app.test_client()

    yield testing_client  # this is where the testing happens!

    with app.app_context():
        db.drop_all()  # Drop tables after tests


def test_user_password():
    """Tests user password hashing and checking."""
    user = User(username="testuser")
    user.set_password("password123")
    assert user.check_password("password123")
    assert not user.check_password("wrongpassword")


def test_task_creation():
    """Tests the creation and retrieval of a task."""
    with app.app_context():  # Ensure app context for db operations
        user = User(username="taskuser")
        user.set_password("pass")
        db.session.add(user)
        db.session.commit()

        task = Task(description="Buy groceries", user_id=user.id)
        db.session.add(task)
        db.session.commit()

        retrieved_task = Task.query.filter_by(description="Buy groceries").first()
        assert retrieved_task is not None
        assert retrieved_task.description == "Buy groceries"
        assert not retrieved_task.completed
        assert retrieved_task.user_id == user.id
