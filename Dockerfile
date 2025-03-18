# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install system dependencies
#RUN apt-get update && apt-get install -y \
#    default-libmysqlclient-dev \
#    gcc \
#    python3-dev \
#    musl-dev \
#    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    python3-dev \
    build-essential \
    pkg-config


# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files
COPY pyproject.toml poetry.lock /app/

# Install dependencies without creating a virtual environment
RUN poetry config virtualenvs.create false && poetry install --no-root --no-cache

# Copy Django app
COPY . /app

# Expose port
EXPOSE 8000

# Change ownership to your user (replace 1000:1000 with your UID:GID)
RUN chown -R 1000:1000 /app

# Start Django server
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
