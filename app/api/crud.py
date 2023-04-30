from sqlalchemy.orm import Session
import app.api.models as models
import app.api.schemas as schemas

# CRUD functions for items

# Create a new item in the database
def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Get an item from the database by ID
def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


# Get all items from the database
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


# Update an item in the database
def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    for field, value in item:
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item


# Delete an item from the database
def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return db_item


# CRUD functions for users

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user: schemas.User):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    for field, value in user:
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user


# CRUD functions for email types

def create_email_type(db: Session, email_type: schemas.EmailTypeCreate):
    db_email_type = models.EmailType(**email_type.dict())
    db.add(db_email_type)
    db.commit()
    db.refresh(db_email_type)
    return db_email_type


def get_email_type(db: Session, email_type_id: int):
    return db.query(models.EmailType).filter(models.EmailType.id == email_type_id).first()


def get_email_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.EmailType).offset(skip).limit(limit).all()


def update_email_type(db: Session, email_type_id: int, email_type: schemas.EmailType):
    db_email_type = db.query(models.EmailType).filter(models.EmailType.id == email_type_id).first()
    for field, value in email_type:
        setattr(db_email_type, field, value)
    db.commit()
    db.refresh(db_email_type)
    return db_email_type


def delete_email_type(db: Session, email_type_id: int):
    db_email_type = db.query(models.EmailType).filter(models.EmailType.id == email_type_id).first()
    db.delete(db_email_type)
    db.commit()
    return db_email_type