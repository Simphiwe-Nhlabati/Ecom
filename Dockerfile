# Use an official Python image as a base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        musl-dev \
        netcat && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application
COPY . /app

# Collect static files
RUN python manage.py collectstatic --noinput


# Command to run your app (can be overridden by docker-compose)
CMD ["gunicorn", "project_name.wsgi:application", "--bind", "0.0.0.0:8000"]
