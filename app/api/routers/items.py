from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.api.schemas as schemas
import app.api.crud as crud
import app.database as database

router = APIRouter()


# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint to create a new item
@router.post("/items", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.create_item(db, item)
    return db_item


# Endpoint to get an item by ID
@router.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


# Endpoint to get all items with optional pagination
@router.get("/items", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# Endpoint to update an item by ID
@router.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item = crud.update_item(db, item_id=item_id, item=item)
    return db_item


# Endpoint to delete an item by ID
@router.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item = crud.delete_item(db, item_id=item_id)
    return db_item


# Endpoint to create a new user
@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return db_user


# Endpoint to get a user by ID
@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Endpoint to get all users with optional pagination
@router.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# Endpoint to update a user by ID
@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = crud.update_user(db, user_id=user_id, user=user)
    return db_user


# Endpoint to delete a user by ID
@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = crud.delete_user(db, user_id=user_id)
    return db_user


# Endpoint to create a new email type
@router.post("/email_types", response_model=schemas.EmailType)
def create_email_type(email_type: schemas.EmailTypeCreate, db: Session = Depends(get_db)):
    db_email_type = crud.create_email_type(db, email_type)
    return db_email_type


# Endpoint to get an email type by ID
@router.get("/email_types/{email_type_id}", response_model=schemas.EmailType)
def read_email_type(email_type_id: int, db: Session = Depends(get_db)):
    db_email_type = crud.get_email_type(db, email_type_id=email_type_id)
    if db_email_type is None:
        raise HTTPException(status_code=404, detail="Email type not found")
    return db_email_type


# Endpoint to get all email types with optional pagination
@router.get("/email_types", response_model=List[schemas.EmailType])
def read_email_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    email_types = crud.get_email_types(db, skip=skip, limit=limit)
    return email_types


# Endpoint to update an email type by ID
@router.put("/email_types/{email_type_id}", response_model=schemas.EmailType)
def update_email_type(
    email_type_id: int, email_type: schemas.EmailType, db: Session = Depends(get_db)
):
    db_email_type = crud.get_email_type(db, email_type_id=email_type_id)
    if db_email_type is None:
        raise HTTPException(status_code=404, detail="Email type not found")
    db_email_type = crud.update_email_type(db, email_type_id=email_type_id, email_type=email_type)
    return db_email_type


# Endpoint to delete an email type by ID
@router.delete("/email-types/{email_type_id}", response_model=schemas.EmailType)
def delete_email_type(email_type_id: int, db: Session = Depends(get_db)):
    db_email_type = crud.get_email_type(db, email_type_id=email_type_id)
    if db_email_type is None:
        raise HTTPException(status_code=404, detail="Email type not found")
    db_email_type = crud.delete_email_type(db, email_type_id=email_type_id)
    return db_email_type
