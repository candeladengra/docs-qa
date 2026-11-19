# Setup Instructions

## Prerequisites

### Required
- Docker Desktop (or Docker + Docker Compose)
- Git

### For local AI (Recommended - Free)
- **Ollama** installed on your host machine
  1. Install from [ollama.ai](https://ollama.ai)
  2. Pull required models:
     ```bash
     ollama pull llama3.2
     ollama pull nomic-embed-text
     ```

### Alternative: Cloud AI
- Google Gemini API key from [makersuite.google.com](https://makersuite.google.com/app/apikey)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd docs-qa
   ```

2. **Configure environment** (optional)
   ```bash
   cp .env.example .env
   # Edit .env if you want to use Gemini instead of Ollama
   ```

3. **Start all services**
   ```bash
   docker-compose up --build
   ```

   First run will take a few minutes to:
   - Build Docker images
   - Download dependencies
   - Run database migrations
   - Create superuser (admin/admin)

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

5. **(Optional) Create superuser for admin access**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## Troubleshooting

### Ollama connection issues
- Make sure Ollama is running: `ollama list`
- On Linux, Ollama URL should be `http://172.17.0.1:11434`
- On macOS/Windows, use `http://host.docker.internal:11434` (default)

### Port conflicts
If ports 5173, 8000, 5432, or 6379 are already in use:
1. Stop other services using those ports
2. Or modify ports in `docker-compose.yml`

### Database issues
Reset database:
```bash
docker-compose down -v  # Delete volumes
docker-compose up --build
```

### Worker not processing documents
Check worker logs:
```bash
docker-compose logs worker
```

## Development

### Backend development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

### Frontend development
```bash
cd frontend
npm install
npm run dev
```

### Running tests locally
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```
