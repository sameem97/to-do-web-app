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
- Set task priorities (Low, Medium, High)
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

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file:

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

**Note:** If running the application locally using `flask run`, you need to set the `FLASK_APP` and `FLASK_DEBUG` environment variables. If running via Docker, these variables are not required as the application is run using Gunicorn.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Deployment and CI/CD

This application is configured for deployment to a Kubernetes cluster emulated by Minikube running on an AWS EC2 instance, with a CI/CD pipeline managed by Jenkins on a separate EC2 instance.

### CI/CD Pipeline

The Jenkins pipeline automates the following steps:

1. Code checkout from GitHub
2. Docker image build with `--no-cache` to ensure fresh builds
3. Running tests in a containerized environment
4. Pushing the Docker image to DockerHub
5. Deploying to Minikube cluster

### Kubernetes Deployment (Minikube on EC2)

A Minikube cluster is set up on an EC2 instance to simulate a Kubernetes environment.

**Prerequisites on EC2:**

- Docker
- Minikube
- kubectl

**Setup Steps:**

1. **Launch EC2 Instance:** Provision an EC2 instance (e.g., Ubuntu 22.04, `t2.medium` or larger for Minikube). Ensure appropriate Security Group rules are in place (e.g., SSH on port 22, HTTP on port 80).

2. **Install Docker:**

    ```bash
    sudo apt update
    sudo apt install docker.io -y
    sudo usermod -aG docker ubuntu # Replace 'ubuntu' with your EC2 user
    newgrp docker # Apply group changes immediately
    ```

3. **Install Minikube and kubectl:**

    ```bash
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    ```

4. **Start Minikube:**

    ```bash
    minikube start --driver=docker
    ```

    *Note: Ensure the Docker image for the application is built for `linux/amd64` architecture (e.g., `docker build --platform linux/amd64 -t todo-app .`) to avoid platform mismatch issues on `amd64` EC2 instances.*

### Jenkins Setup

The Jenkins server is configured with the following credentials:

- DockerHub credentials for image pushing
- GitHub credentials for code checkout
- SSH key for Minikube deployment
- Environment variables (SECRET_KEY, DATABASE_URL)

The pipeline is triggered automatically on pushes to the main branch.