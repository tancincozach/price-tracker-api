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

COPY . .

ENV DJANGO_SETTINGS_MODULE=app.settings

RUN ls -la /app

RUN ls -la /app/staticfiles || echo "No staticfiles directory"

RUN python manage.py collectstatic --noinput

EXPOSE 8000

RUN pip install uvicorn

CMD ["uvicorn", "app.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
