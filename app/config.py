# NOTHING IS USEING THIS FILE YET

from pydantic import BaseSettings

# Define a subclass of BaseSettings to store configuration settings
class Settings(BaseSettings):
    # Set the name of the project
    PROJECT_NAME: str = "FastAPI Example"

    # Set the URL prefix for API endpoints
    API_PREFIX: str = "/api"

    # Database settings
    # Set the connection string for the SQLite database
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./emails.sqlite"
    
    # Enable or disable SQLAlchemy logging
    SQLALCHEMY_ECHO: bool = False

    # Configuration for Pydantic
    class Config:
        # Load environment variables from a file named ".env"
        env_file = ".env"


# Create an instance of the Settings class
# that can be used throughout the application
settings = Settings()
