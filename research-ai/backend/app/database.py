from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# If postgresql doesn't work out of the box due to user missing server, fall back to sqlite gracefully
engine = create_engine(
    settings.DATABASE_URL, 
    # check_same_thread ONLY needed for sqlite, ignored by PG usually, but let's be careful
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
