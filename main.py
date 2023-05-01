from fastapi import FastAPI
from app.api.routers import items_router
# from app.database import engine
# from app.models.models import Base
from app.api.routers import api_router

# Create the FastAPI application instance
app = FastAPI()

# Include the endpoint routes
app.include_router(api_router)
