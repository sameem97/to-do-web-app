FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create instance directory and set permissions
RUN mkdir -p /app/instance && \
    chmod 775 /app/instance && \
    chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 5000

# Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]