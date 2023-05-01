from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.schemas.email_type as schemas
import app.middleware.crud.emailType_crud as crud
import app.database as database

emailType_router = APIRouter()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint to create a new email type
@emailType_router.post("/email_types", response_model=schemas.EmailType)
def create_email_type(email_type: schemas.EmailTypeCreate, db: Session = Depends(get_db)):
    db_email_type = crud.create_email_type(db, email_type)
    return db_email_type


# Endpoint to get an email type by ID
@emailType_router.get("/email_types/{email_type_id}", response_model=schemas.EmailType)
def read_email_type(email_type_id: int, db: Session = Depends(get_db)):
    db_email_type = crud.get_email_type(db, email_type_id=email_type_id)
    if db_email_type is None:
        raise HTTPException(status_code=404, detail="Email type not found")
    return db_email_type


# Endpoint to get all email types with optional pagination
@emailType_router.get("/email_types", response_model=List[schemas.EmailType])
def read_email_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    email_types = crud.get_email_types(db, skip=skip, limit=limit)
    return email_types


# Endpoint to update an email type by ID
@emailType_router.put("/email_types/{email_type_id}", response_model=schemas.EmailType)
def update_email_type(
    email_type_id: int, email_type: schemas.EmailType, db: Session = Depends(get_db)
):
    db_email_type = crud.get_email_type(db, email_type_id=email_type_id)
    if db_email_type is None:
        raise HTTPException(status_code=404, detail="Email type not found")
    db_email_type = crud.update_email_type(db, email_type_id=email_type_id, email_type=email_type)
    return db_email_type


# Endpoint to delete an email type by ID
@emailType_router.delete("/email_types/{email_type_id}", response_model=schemas.EmailType)
def delete_email_type(email_type_id: int, db: Session = Depends(get_db)):
    db_email_type = crud.get_email_type(db, email_type_id=email_type_id)
    if db_email_type is None:
        raise HTTPException(status_code=404, detail="Email type not found")
    db_email_type = crud.delete_email_type(db, email_type_id=email_type_id)
    return db_email_type


# Endpoint to get all email addresses subscribed to an email type
@emailType_router.get("/email_types/{email_type_id}/subscriptions", response_model=List)
def get_subscriptions_by_email_type(email_type_id: int, db: Session = Depends(get_db)):
    
    # Check that the email type exists
    email_type = crud.get_email_type(db, email_type_id=email_type_id)
    if not email_type:
        raise HTTPException(status_code=404, detail="Email type not found")

    # Get the users subscribed to the email type
    email_distro = crud.get_subscriptions_by_emailID(db, email_type_id=email_type_id)
    
    # return a list of email addresses subscribed to the email type
    return email_distro