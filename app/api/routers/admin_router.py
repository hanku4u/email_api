from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import app.schemas.user as schemas
import app.models.models as models
import app.oauth2 as oauth2
import utils

admin_router = APIRouter()


@admin_router.post('/admin_login')
# OAuth2PasswordRequestForm is a class that has two attributes: username and password stored in user_credentials
def admin_login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(utils.get_db)
    ):

    # get the user from the database
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # if the user is not found, raise an exception
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    # if the user is found, check the password
    if not utils.verify(hashed_password=user.hashed_pw, plain_password=user_credentials.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    # create a token for the user. data is the user fields you want to encode into the token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # if the user is found and the password is correct, return the access token
    return {'access_token': access_token, 'token_type': 'bearer'}