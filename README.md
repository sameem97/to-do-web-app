# Todo Web Application

A simple todo web application with user authentication and task management, built with Flask.

## Project Structure

```txt
to-do-web-app/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── entrypoint.sh      # Docker entrypoint script
├── .env.example       # Example environment variables
├── instance/          # Instance-specific files (database)
└── templates/         # HTML templates
```

## Features

- User authentication (register, login, logout)
- Create, read, update, and delete tasks
- Set due dates for tasks
- Mark tasks as complete/incomplete
- Responsive design

## Views

![Todo App Dashboard](images/dashboard.png)
*Main dashboard showing task management interface*

![Login Page](images/login.png)
*User login interface*

![Register Page](images/register.png)
*New user registration form*

## Prerequisites

- Python 3.11 or higher
- Docker (optional, for containerized deployment)

## Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd to-do-web-app
```

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Create a `.env` file:

```bash
cp .env.example .env
```

Then edit `.env` and set your own `SECRET_KEY`.

## Running the Application

### Local Development

Run the application in debug mode:

```bash
flask run --debug
```

The application will be available at <http://127.0.0.1:5000>

### Docker Deployment

Build and run the Docker container:

```bash
docker build -t todo-app .
docker run -p 5000:5000 --env-file .env todo-app
```

The application will be available at <http://localhost:5000>

## Environment Variables

- `SECRET_KEY`: Secret key for session management
- `DATABASE_URL`: SQLite database URL (default: sqlite:///instance/todo.db)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
