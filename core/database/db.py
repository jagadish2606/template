from sqlmodel import create_engine, Session
from sqlalchemy.pool import NullPool
from core.config import DATABASE_URL

def get_db():
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, poolclass=NullPool)
    try:
        db = Session(bind=engine, autoflush=False)
        yield db
    finally:
        db.close()




