from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
import app.schemas.user as schemas
import app.models.models as models
import utils

admin_router = APIRouter()


@admin_router.post('/admin_login')
def admin_login(user_credentials: schemas.UserLogin, db: Session = Depends(utils.get_db)):

    # get the user from the database
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    # if the user is not found, raise an exception
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    
    # if the user is found, check the password
    if not utils.verify(hashed_password=user.hashed_pw, plain_password=user_credentials.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")
    
    # TODO create a token for the user

    # if the user is found and the password is correct, return the user
    return {'token': 'example_token'}