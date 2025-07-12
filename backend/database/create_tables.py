"""
Script to initialize and create all database tables defined in SQLAlchemy models.
This is typically run once during setup or migrations to bootstrap the schema.
"""

from backend.database.db_connection import engine, Base
from backend.database import db_models  # Ensure all models are imported so SQLAlchemy picks them up

def initialize_tables():
    """Create all tables in the database based on the SQLAlchemy models."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    initialize_tables()
