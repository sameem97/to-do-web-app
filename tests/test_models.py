# tests/test_models.py
import pytest
import os
from dotenv import load_dotenv
from app import create_app, User, Task, db  # Import the global db instance

# Load environment variables from .env file if it exists
load_dotenv()


@pytest.fixture(scope="function")
def test_client():
    """Configures the Flask app for testing and sets up an in-memory database."""
    app = create_app(  # Only capture app since we use the global db
        {
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "TESTING": True,
            "SECRET_KEY": os.getenv("SECRET_KEY") or os.urandom(24).hex(),
        }
    )

    with app.app_context():
        db.create_all()

    yield app  # Yield the app instance

    with app.app_context():
        db.drop_all()


def test_user_password(test_client):  # test_client is the app instance
    """Tests user password hashing and checking."""
    app = test_client  # Alias for clarity
    with app.app_context():
        user = User(username="testuser")
        user.set_password("password123")
        db.session.add(user)  # Use the globally imported db.session
        db.session.commit()
        assert user.check_password("password123")
        assert not user.check_password("wrongpassword")


def test_task_creation(test_client):  # test_client is the app instance
    """Tests the creation and retrieval of a task."""
    app = test_client  # Alias for clarity
    with app.app_context():
        user = User(username="taskuser")
        user.set_password("pass")
        db.session.add(user)  # Use the globally imported db.session
        db.session.commit()

        task = Task(description="Buy groceries", user_id=user.id)
        db.session.add(task)  # Use the globally imported db.session
        db.session.commit()

        retrieved_task = (
            db.session.query(Task).filter_by(description="Buy groceries").first()
        )  # Use the globally imported db.session
        assert retrieved_task is not None
        assert retrieved_task.description == "Buy groceries"
        assert not retrieved_task.completed
        assert retrieved_task.user_id == user.id
