# PyBazaar App

## Prerequisites
Ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Set Up Environment Variables
Copy the example environment file and update it with your configurations:
```bash
cp .env.example .env
```
Modify `.env` as needed.

### 3. Build and Start the Containers
```bash
docker-compose up --build
```
This command will build the necessary Docker images and start the containers in detached mode.

### 4. Run Migrations & Collect Static Files
```bash
docker-compose exec web poetry run python manage.py migrate
```

[//]: # (### 5. Create a Superuser)

[//]: # (```bash)

[//]: # (docker-compose exec web poetry run python manage.py createsuperuser)

[//]: # (```)

[//]: # (Follow the prompts to create an admin user.)

### 6. Access the Application
- The app will be running at: `http://localhost:8005`

[//]: # (- Django Admin: `http://localhost:8000/admin`)

## Running Commands inside the Docker Container
To run any Django command inside the container, use:
```bash
docker-compose exec web poetry run python manage.py <command>
```

## Stopping and Restarting the Containers
```bash
docker-compose down  # Stop containers
```
```bash
docker-compose up -d  # Restart containers
```

## Logs
To view logs:
```bash
docker-compose logs -f <container-name>
```

[//]: # (## Running Tests)

[//]: # (```bash)

[//]: # (docker-compose exec web poetry run pytest)

[//]: # (```)

## Cleanup
To remove all containers, volumes, and images:
```bash
docker-compose down -v
```

