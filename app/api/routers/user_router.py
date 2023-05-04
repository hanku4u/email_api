from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.schemas.user as schemas
import app.middleware.crud.user_crud as user_crud
import app.middleware.crud.emailType_crud as email_type_crud
import app.database as database
from logger import logger

user_router = APIRouter()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint to create a new user
@user_router.post("/new_user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(db, user)

    # log success
    logger.info(f'Endpoint: /new_user, Method: POST, Status: Success')

    # return new user object
    return db_user


# Endpoint to get a user by ID
@user_router.get("/read_user/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    # check if user ID passed exists in DB
    db_user = user_crud.get_user(db, user_id=user_id)

    if db_user is None:
        # log failure
        logger.error(f'Endpoint: /read_user, User ID:{user_id}, Method: GET, Status: Failed, ID not found')
        raise HTTPException(status_code=404, detail="User not found")

    # log success
    logger.info(f'Endpoint: /read_user, User ID:{user_id}, Method: GET, Success')

    # return found user object
    return db_user


# Endpoint to get all users with optional pagination
@user_router.get("/all_users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    
    # log success
    logger.info(f'Endpoint: /all_users, Method: GET, Status: Success')

    # return list of found user objects
    return users


# Endpoint to update a user by ID
@user_router.put("/update_user/{user_id}", response_model=schemas.User)
def update_user_by_id(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    # look up user_id that was passed exists
    db_user = user_crud.get_user(db, user_id=user_id)

    if db_user is None:
        # log failure
        logger.error(f'Endpoint: /update_user, User ID:{user_id}, Method: GET, Status: Failed, ID not found')
        raise HTTPException(status_code=404, detail="Item not found")
    
    # call crud function to update the user
    result = user_crud.update_user(db, user_id=user_id, user=user_update)

    # log success
    logger.info(f'Endpoint: /update_user, User ID:{user_id}, Method: GET, Success')

    return result  # Return the updated user object


# Endpoint to delete a user by ID
@user_router.delete("/delete_user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # check if user_id passed exists in DB
    db_user = user_crud.get_user(db, user_id=user_id)

    if db_user is None:
        # log failure
        logger.error(f'Endpoint: /delete_user, User ID:{user_id}, Method: DELETE, Status: Failed, ID not found')
        raise HTTPException(status_code=404, detail="User not found")

    # delete user
    db_user = user_crud.delete_user(db, user_id=user_id)

    # log success
    logger.info(f'Endpoint: /delete_user, User ID:{user_id}, Method: DELETE, Status: Success')

    return db_user


# Endpoint to subscribe a user to email types
@user_router.post("/update_user/{user_id}/subscribe", response_model=schemas.User)
def subscribe_user_to_email_types(
    user_id: int, 
    email_type_ids: List[int],
    db: Session = Depends(get_db)
):
    # Check that the user exists
    user = user_crud.get_user(db, user_id=user_id)
    if not user:
        # log failure
        logger.error(f'Endpoint: /update_user/id/subscribe, User ID:{user_id}, Method: POST, Status: Failed, User ID not found')
        raise HTTPException(status_code=404, detail="User not found")

    # Check that all email types exist
    email_types = email_type_crud.get_email_types_by_ids(db, email_type_ids)
    if not email_types:
        # log failure
        logger.error(f'Endpoint: /update_user/id/subscribe, User ID:{email_type_ids}, Method: POST, Status: Failed, Email ID not found')
        raise HTTPException(status_code=404, detail="Email types not found")
    
    # Get the ids of the email types and put them in a list
    found_email_ids = [email_type.id for email_type in email_types]

    # Subscribe the user to the email types
    result = user_crud.subscribe_user_to_email_types(db, user.id, found_email_ids)

    # log success
    logger.info(f'Endpoint: /update_user/id/subscribe, User ID:{user_id}, Method: POST, Status: Success')
    return result
