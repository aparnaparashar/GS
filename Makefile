# Makefile for GeoSense (Option A)
# Usage: make <target>
# Recommended: use Docker-based targets for consistent environment.

.PHONY: all build up down restart logs frontend-install backend-shell db-shell init-db clean

all: build

build:
	@echo "Building backend and frontend Docker images..."
	docker-compose build

up:
	@echo "Starting services (build if necessary)..."
	docker-compose up -d --build

down:
	@echo "Stopping services..."
	docker-compose down

restart: down up

logs:
	@echo "Tailing logs (backend)..."
	docker-compose logs -f backend

frontend-install:
	@echo "Install frontend dependencies locally (optional)"
	cd frontend && npm install

backend-shell:
	@echo "Open a shell into the backend container"
	docker-compose exec backend /bin/bash

db-shell:
	@echo "Open a psql shell into the db container"
	docker-compose exec db psql -U postgres -d geosense

init-db:
	@echo "Initialize PostGIS extensions (run once after DB is up)"
	@echo "Connecting to db and creating extensions..."
	docker-compose exec db bash -c "psql -U postgres -d geosense -c "CREATE EXTENSION IF NOT EXISTS postgis;" && psql -U postgres -d geosense -c "CREATE EXTENSION IF NOT EXISTS postgis_topology;""

clean:
	@echo "Removing built images (use with caution)"
	docker-compose down --rmi local --volumes
