from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/jarvis")

# Try to connect to the configured DB; if unavailable, fallback to a local SQLite file for dev.
try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    # quick test connection
    conn = engine.connect()
    conn.close()
except Exception:
    sqlite_url = os.environ.get("JARVIS_SQLITE_URL", "sqlite:///./jarvis.db")
    engine = create_engine(sqlite_url, connect_args={"check_same_thread": False} if sqlite_url.startswith("sqlite") else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
