from sqlalchemy import event, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from app.config import get_settings
from sqlalchemy.ext.declarative import declarative_base


# # SQLALCHEMY_DATABASE_URL = "sqlite:///./emails.sqlite"  # Database URL for SQLite
# # SQLALCHEMY_DATABASE_URL = "sqlite:///mnt/n.haight/s3/emailAPI/email-api.sqlite"

# # Create a SQLAlchemy engine to connect to the database
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# # Create a SessionLocal class for creating database sessions
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, _):
    """sets the pragma options when the db connections"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")  # enable WAL
    cursor.execute("PRAGMA foreign_keys=ON;")  # enforce foreign keys
    dbapi_connection.commit()
    cursor.close()


# setup the engine
settings = get_settings()
engine = create_engine(
    settings.DATABASE_URI,
    # required for sqlite
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a declarative base class for database models
Base = declarative_base()
