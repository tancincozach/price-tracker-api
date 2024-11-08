# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies, including PostgreSQL client
RUN apt-get update \
    && apt-get install -y \
    build-essential \
    libpq-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=app.settings

# Debugging step: List contents of /app
RUN ls -la /app

# Debugging step: List contents of /app/staticfiles
RUN ls -la /app/staticfiles || echo "No staticfiles directory"

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000 for the application
EXPOSE 8000

# Install Uvicorn
RUN pip install uvicorn

# Run the application with Uvicorn
CMD ["uvicorn", "app.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
