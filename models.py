# models.py
"""
SQLAlchemy models and database setup for GameStatDarksiders.
Uses SQLite by default (database.db).
If you want to use MS SQL Server, see the commented example below.
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    weapon = Column(String(100), nullable=False)
    level = Column(Integer, nullable=False, default=1)
    realm = Column(String(100), nullable=False)

# Default SQLite engine (file: database.db)
SQLITE_URL = "sqlite:///database.db"
engine = create_engine(SQLITE_URL, echo=False, future=True)

# If you want to connect to MS SQL Server instead, uncomment and adapt:
# NOTE: you'll need 'pyodbc' installed and the correct ODBC driver on your machine.
# Example:
# MSSQL_URL = "mssql+pyodbc://username:password@SERVER_NAME/DatabaseName?driver=ODBC+Driver+17+for+SQL+Server"
# engine = create_engine(MSSQL_URL, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, future=True)

def init_db():
    Base.metadata.create_all(bind=engine)

# Initialize DB on import (creates database.db if not present)
init_db()
