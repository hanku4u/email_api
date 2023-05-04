from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.schemas.email_type as schemas
import app.middleware.crud.emailType_crud as crud
import app.database as database
from logger import logger

emailType_router = APIRouter()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint to create a new email type
@emailType_router.post("/create_email", response_model=schemas.EmailType)
def create_email_type(email_type: schemas.EmailTypeCreate, db: Session = Depends(get_db)):
    db_email_type = crud.create_email_type(db, email_type)
    # log success
    logger.info('Endpoint: /create_email, Method: POST, Status: Success')

    # return new email type object
    return db_email_type


# Endpoint to get an email type by ID
@emailType_router.get("/get_email/{email_type_id}", response_model=schemas.EmailType)
def read_email_type(email_type_id: int, db: Session = Depends(get_db)):
    # check db if passed ID exists
    db_email_type = crud.get_email_type(db, email_type_id=email_type_id)
    
    if db_email_type is None:
        logger.error(f'Endpoint: /get_email, ID:{email_type_id}, Method: GET, Status: Failed, ID not found')
        raise HTTPException(status_code=404, detail="Email type not found")

    # log success
    logger.info(f'Endpoint: /get_email, ID:{email_type_id}, Method: GET, Status: Success')

    # return email found in DB
    return db_email_type


# Endpoint to get all email types with optional pagination
@emailType_router.get("/all_emails", response_model=List[schemas.EmailType])
def read_email_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # get email types from DB
    email_types = crud.get_email_types(db, skip=skip, limit=limit)

    # log success
    logger.info('Endpoint: /all_emails, Method: GET, Status: Success')
    
    # return list of email types
    return email_types


# Endpoint to update an email type by ID
@emailType_router.put("/update_email/{email_type_id}", response_model=schemas.EmailType)
def update_email_type(
    email_type_id: int, email_type: schemas.EmailTypeUpdate, db: Session = Depends(get_db)
):
    # check db if email ID exists
    db_email_type = crud.get_email_type(db, email_type_id=email_type_id)
    
    if db_email_type is None:
        # log failure
        logger.error('Endpoint: /update_email by ID, Method: PUT, Status: Failed, ID not found')
        raise HTTPException(status_code=404, detail="Email type not found")

    # update in DB
    db_email_type = crud.update_email_type(db, email_type_id=email_type_id, email_type=email_type)

    # log success
    logger.info('Endpoint: /update_email by ID, Method: GET, Status: Success')

    # return updated email object
    return db_email_type


# Endpoint to delete an email type by ID
@emailType_router.delete("/delete_email/{email_type_id}")
def delete_email_type(email_type_id: int, db: Session = Depends(get_db)):
    # check DB if email_type_id pass exists
    db_email_type = crud.get_email_type(db, email_type_id=email_type_id)

    if db_email_type is None:
        # log failure
        logger.error(f'Endpoint: /delete_email, ID:{email_type_id}, Method: DELETE, Status: Failed, ID not found')
        raise HTTPException(status_code=404, detail="Email type not found")

    # update email type in DB
    db_email_type = crud.delete_email_type(db, email_type_id=email_type_id)

    # log success
    logger.info(f'Endpoint: /delete_email, ID:{email_type_id}, Method: DELETE, Status: Success')

    # return success message
    return {"Email type deleted successfully"}


# Endpoint to get all email addresses subscribed to an email type
@emailType_router.get("/get_email/{email_type_id}/subscriptions", response_model=List)
def get_subscriptions_by_email_type(email_type_id: int, db: Session = Depends(get_db)):
    
    # Check that the email type exists
    email_type = crud.get_email_type(db, email_type_id=email_type_id)
    if not email_type:
        # log failure
        logger.error(f'Endpoint: /get_email subscriptions, ID:{email_type_id}, Method: GET, Status: Failed, ID not found')
        raise HTTPException(status_code=404, detail="Email type not found")

    # Get the users subscribed to the email type
    email_distro = crud.get_subscriptions_by_emailID(db, email_type_id=email_type_id)

    # log success
    logger.info(f'Endpoint: /get_email subscriptions, ID:{email_type_id}, Method: GET, Status: Success')
    
    # return a list of email addresses subscribed to the email type
    return email_distro
