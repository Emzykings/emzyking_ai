from backend.database.db_connection import engine, Base
from backend.database import db_models

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
