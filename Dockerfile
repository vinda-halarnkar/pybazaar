# Use official Python image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Install Poetry globally
RUN pip install --no-cache-dir poetry

# Copy only the dependency files first (improves caching)
COPY pyproject.toml poetry.lock /app/

# Install dependencies in a virtual environment
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-cache

# Copy the rest of the application
COPY . /app

# Expose the Flask port (default 5000)
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Command to run the app
#CMD ["poetry", "run", "python", "run.py"]

RUN chown -R 1000:1000 /app
