# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files (optional, if you serve static from Django)
RUN python manage.py collectstatic --noinput

# Expose port (optional)
EXPOSE 8000

# Run migrations and start ASGI server with Daphne
CMD ["bash", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 chat_room.asgi:application"]
