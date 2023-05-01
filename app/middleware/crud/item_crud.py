from sqlalchemy.orm import Session
import app.models.models as models
import app.schemas.item as schemas


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