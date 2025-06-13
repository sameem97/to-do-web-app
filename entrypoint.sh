#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Navigate to the application directory
cd /app

# Ensure the instance directory exists and has correct permissions
mkdir -p instance
chmod 775 instance

# Create database tables
python3 -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
"

# Start the application using gunicorn
# The app:app refers to the 'app' variable in the 'app.py' module
# Since create_app is called in app.py's __main__ block, it should be available
exec gunicorn --bind 0.0.0.0:5000 app:app 