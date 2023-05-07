from passlib.context import CryptContext
import app.database as database

# define the context for hashing passwords. use bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# define a function to hash a password
def hash(password: str):
    """Hash a password for storing."""
    return pwd_context.hash(password)


# define a function to verify a password
def verify(hashed_password, plain_password):
    """Verify a stored password against one provided by user"""
    return pwd_context.verify(plain_password, hashed_password)


# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
