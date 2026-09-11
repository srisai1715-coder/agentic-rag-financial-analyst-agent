# Phase 16 — PostgreSQL Integration

## Goal

Add PostgreSQL as the application database while keeping Qdrant as the vector database.

- Qdrant → embeddings + semantic document retrieval
- PostgreSQL → application-level agent run storage and metadata

## ADD

- `app/database/postgres.py`
- `tests/test_postgres.py`
- `PHASE_16.md`

## REPLACE

- `app/main.py`
- `docker-compose.yml`

The replacement files preserve the existing FastAPI router and CORS setup and add PostgreSQL startup initialization plus a PostgreSQL service.

## KEEP

Keep all other existing project files unchanged, including:

- `app/api/routes.py`
- `app/agent/`
- `app/rag/`
- `app/tools/`
- `app/llm/`
- `app/observability/`
- `data/`
- `tests/`
- `evaluation/`
- `frontend/`
- `.env`
- Dockerfile
- Qdrant data

Do not delete Qdrant data.

## 1. Add the dependency

Open `requirements.txt` and add this single line:

```text
psycopg[binary]>=3.2,<4
```

Do not remove existing dependencies.

Then install it in the local environment:

```powershell
python -m pip install "psycopg[binary]>=3.2,<4"
```

## 2. Environment

Your `.env` can contain the local PostgreSQL URL:

```text
DATABASE_URL=postgresql://financial_agent:financial_agent@localhost:5432/financial_agent
```

Do not share API keys.

Inside Docker Compose, the API automatically uses the internal hostname `postgres`, so you do not need to change `.env` for the container.

## 3. Build and start

From the project root:

```powershell
docker compose down
docker compose build
docker compose up
```

PostgreSQL will start as a separate container and the API will wait for its health check.

The database table `agent_runs` is initialized automatically by FastAPI startup.

## 4. Verify PostgreSQL

In another PowerShell terminal:

```powershell
docker compose ps
```

You should see both:

- `api`
- `postgres`

Then:

```powershell
docker compose exec postgres psql -U financial_agent -d financial_agent -c "\dt"
```

You should see the `agent_runs` table.

## 5. Verify API

```powershell
Invoke-RestMethod http://localhost:8000/health
```

The API should still return:

```text
status  service
healthy financial-analyst-agent
```

Your React frontend remains at:

`http://localhost:5173`

## 6. Run tests

From the project root:

```powershell
python -m pytest -q
```

## Important architecture

Do not store embeddings in PostgreSQL.

```text
PDF
 ↓
Embeddings
 ↓
Qdrant ──────────→ RAG retrieval

Agent/API
 ↓
PostgreSQL ───────→ application data
```

This phase establishes PostgreSQL infrastructure and the application persistence layer. The next phase can build on this without changing Qdrant.
