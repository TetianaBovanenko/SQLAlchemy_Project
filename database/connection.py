from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL, logger

# Create engine and session
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)


def get_session():
    """Return a new session."""
    return Session()


def initialize_database():
    """Initialize the database."""
    from models.base import Base
    from models.user import User  # Import all models here

    logger.info("Creating tables in the database...")
    Base.metadata.create_all(engine)
    logger.info("Database tables created successfully.")
