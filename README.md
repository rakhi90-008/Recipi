# Recipes Stack (Backend + UI + Docker)

This bundle includes:
- **Backend** (FastAPI + SQLAlchemy + Postgres) in `backend/`
- **Data** (US_recipes.json) in `data/` (included if you uploaded it)
- **React UI** (Vite) in `frontend/`
- **Docker Compose** to run everything

## Quickstart (Docker)
```bash
docker compose up --build -d
# Load data into Postgres
docker compose exec api python load_data.py
# Open UI
# http://localhost:5173  (UI)  — talks to http://localhost:8000
# Health check
curl http://localhost:8000/api/health
```
To reload data after changing `data/US_recipes.json`:
```bash
docker compose exec api python load_data.py
```

## Local Dev (no Docker)
**DB:** Create a Postgres database and set `DATABASE_URL` in `backend/.env` (copy `.env.example`).  
**Install & run API:**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
psql "$DATABASE_URL" -f schema.sql
python load_data.py
uvicorn app:app --reload
```
**Run UI:**
```bash
cd ../frontend
npm install
npm run dev
# visit http://localhost:5173
```

## API Endpoints
- `GET /api/health` – health check
- `GET /api/recipes?page=1&limit=10` – paginated list sorted by rating
- `GET /api/recipes/search?title=pie&rating=>=4.5&calories=<=400&total_time=<=60&cuisine=Southern%20Recipes`

## Notes
- NaN/invalid numerics become `NULL` in DB.
- Calories filter extracts digits from e.g. `"389 kcal"` to compare as integers.
- Adjust UI page size (15–50) via the dropdown.
