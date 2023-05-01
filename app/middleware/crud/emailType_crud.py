from sqlalchemy.orm import Session
import app.models.models as models
import app.schemas.email_type as schemas


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