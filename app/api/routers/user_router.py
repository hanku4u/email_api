from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.schemas.user as schemas
import app.middleware.crud.user_crud as user_crud
import app.middleware.crud.emailType_crud as email_type_crud
import app.database as database

user_router = APIRouter()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint to create a new user
@user_router.post("/create_user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(db, user)
    return db_user


# Endpoint to get a user by ID
@user_router.get("/get_user/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Endpoint to get all users with optional pagination
@user_router.get("/get_all_users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


# # Endpoint to update a user by ID
# @user_router.put("/update_user/{user_id}", response_model=schemas.User)
# def update_user(user_id: int, user: schemas.User, db: Session = Depends(get_db)):
#     db_user = user_crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     db_user = user_crud.update_user(db, user_id=user_id, user=user)
#     return db_user


@user_router.put("/update_user/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)

    # first check if the user exists
    if db_user is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # call crud function to update the user
    result = user_crud.update_user(db, user_id=user_id, user=user_update)

    return result  # Return the updated user object



# Endpoint to delete a user by ID
@user_router.delete("/delete_user/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = user_crud.delete_user(db, user_id=user_id)
    return db_user


# Endpoint to subscribe a user to email types
@user_router.post("/users/{user_id}/subscribe", response_model=schemas.User)
def subscribe_user_to_email_types(
    user_id: int, 
    email_type_ids: List[int],
    db: Session = Depends(get_db)
):
    # Check that the user exists
    user = user_crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check that all email types exist
    email_types = email_type_crud.get_email_types_by_ids(db, email_type_ids)
    if not email_types:
        raise HTTPException(status_code=404, detail="Email types not found")
    
    # Get the ids of the email types and put them in a list
    found_email_ids = [email_type.id for email_type in email_types]

    # Subscribe the user to the email types
    result = user_crud.subscribe_user_to_email_types(db, user.id, found_email_ids)
    return result