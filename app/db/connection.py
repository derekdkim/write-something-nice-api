from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..settings import env

SQL_DB_URL = f'postgresql://{env.pg_username}:{env.pg_password}@{env.pg_port}/{env.pg_db_name}'

engine = create_engine(SQL_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def connect_db():
    """Middleware to give access to PostgreSQL DB"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
