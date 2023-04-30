from fastapi import FastAPI
from app.api.routers import items
from app.database import engine
from app.api.models import Base

# Create the FastAPI application instance
app = FastAPI()

# Create the database tables
# Base.metadata.create_all(bind=engine)

# Include the endpoint routes
app.include_router(items.router)
