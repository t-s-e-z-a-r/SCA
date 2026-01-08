# Spy Cat Agency (SCA) Management System

A RESTful API application for managing spy cats, their missions, and targets. Built with FastAPI and PostgreSQL.

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (if running without Docker)

## Setup Instructions

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/t-s-e-z-a-r/SCA.git
   cd SCA
   ```

2. **Start all services**
   ```bash
   docker-compose up
   ```
   
   Or run in detached mode:
   ```bash
   docker-compose up -d
   ```

3. **Access the API**
   - API: http://localhost:8000
   - Interactive API docs (Swagger): http://localhost:8000/docs
   - Alternative API docs (ReDoc): http://localhost:8000/redoc

### Running Without Docker

1. **Start PostgreSQL database** (ensure PostgreSQL is running locally)

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables** (optional, defaults are used if not set)
   ```bash
   export DATABASE_URL=postgresql://spycat:spycat123@localhost:5432/spycat_agency
   export THECATAPI_BASE_URL=https://api.thecatapi.com/v1
   ```

4. **Run the application**
   ```bash
   uvicorn backend.main:app --reload
   ```

## API Endpoints

### Spy Cats

- `POST /cats` - Create a new spy cat
- `GET /cats` - List all spy cats
- `GET /cats/{cat_id}` - Get a single spy cat
- `PATCH /cats/{cat_id}` - Update a spy cat's salary
- `DELETE /cats/{cat_id}` - Delete a spy cat (only if no active mission)

### Missions

- `POST /missions` - Create a new mission with targets (1-3 targets required)
- `GET /missions` - List all missions
- `GET /missions/{mission_id}` - Get a single mission with targets
- `PATCH /missions/{mission_id}` - Assign/unassign a cat to/from a mission
- `DELETE /missions/{mission_id}` - Delete a mission (only if not assigned to a cat)
- `PATCH /missions/{mission_id}/targets/{target_id}` - Update target notes or mark as complete

## Postman Collection

A Postman collection is available with all endpoints pre-configured.

[Postman Collection](https://kredo-rd.postman.co/workspace/New-Team-Workspace~ef4d2d98-a2ce-4cb7-ab9a-b8c772d59eda/collection/28347427-b3bbdb1a-24b9-4441-97f8-14d5d7346328?action=share&source=copy-link&creator=28347427)

