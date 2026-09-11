from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import APP_NAME
from app.database.postgres import initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # PostgreSQL is application storage; Qdrant remains the vector database.
    try:
        initialize_database()
    except Exception:
        # Keep the API usable when PostgreSQL is intentionally unavailable,
        # for example during lightweight local unit tests.
        pass
    yield


app = FastAPI(
    title="Financial Analyst Agent",
    version="0.4.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "healthy", "service": APP_NAME}
