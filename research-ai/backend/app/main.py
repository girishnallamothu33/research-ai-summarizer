from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import endpoints
from app.database import engine, Base

# Create DB tables (in a real app you might use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Research Paper Summarization API",
    description="Multi-Disciplinary Knowledge Discovery API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Research Paper Summarization API"}
