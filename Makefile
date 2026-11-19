.PHONY: help build up down clean test test-backend test-frontend logs restart

help:
	@echo "Docs Q&A - Available commands:"
	@echo "  make build          - Build all Docker images"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make clean          - Stop and remove all containers, volumes"
	@echo "  make test           - Run all tests"
	@echo "  make test-backend   - Run backend tests"
	@echo "  make test-frontend  - Run frontend tests"
	@echo "  make logs           - Show logs from all services"
	@echo "  make restart        - Restart all services"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "Frontend: http://localhost:5173"
	@echo "Backend:  http://localhost:8000"
	@echo "Admin:    http://localhost:8000/admin (admin/admin)"

down:
	docker-compose down

clean:
	docker-compose down -v
	@echo "✅ All containers and volumes removed"

test: test-backend test-frontend

test-backend:
	cd backend && pytest

test-frontend:
	cd frontend && npm test -- --run

logs:
	docker-compose logs -f

restart: down up
