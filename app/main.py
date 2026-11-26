from contextlib import asynccontextmanager
import os

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

raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
allowed_origins = [
    origin.strip() for origin in raw_origins.split(",") if origin.strip()
]
if "http://localhost:5173" not in allowed_origins:
    allowed_origins.append("http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "healthy", "service": APP_NAME}