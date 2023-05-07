from fastapi import APIRouter, Depends, HTTPException
from app.api.routers import (
    emailType_router,
    items_router,
    user_router,
    admin_router
)

api_router = APIRouter()

api_router.include_router(emailType_router.emailType_router, prefix="/emailType", tags=["emailType"])
api_router.include_router(items_router.items_router, prefix="/items", tags=["items"])
api_router.include_router(user_router.user_router, prefix="/user", tags=["user"])
api_router.include_router(admin_router.admin_router, prefix="/admin", tags=["admin"])
