from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.schemas import user as schemas
from app.models import models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import utils


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='admin_login')  # create an OAuth2 scheme

# SECRET_KEY
# in terminal run: openssl rand -hex 32 to generate a secret key
SECRET_KEY = '9fe43152dadcf1988993c1b3ee377ad735f947a77d17f931dc8c6802bc754507'

# ALGORITHM
ALGORITHM = 'HS256'

# ACCESS_TOKEN_EXPIRE_MINUTES
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# create access token
def create_access_token(data: dict):
    """Create an access token for the user"""

    # create a copy of the data
    to_encode = data.copy()

    # add expiration to the token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # add the expiration to the token
    to_encode.update({'exp': expire})

    # encode the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt  # return the token


# verify the token
def verify_access_token(token: str, credentials_exception):
    """Verify the access token"""

    try:
        # decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # get the user's login id. in this case, the user's email
        id: str = payload.get('user_id')

        # check if the email exists
        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(user_id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data


# get the current user returns the users DB id
def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(utils.get_db)):
    """Get the current user"""

    # create a credentials exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    # verify the token
    token = verify_access_token(token, credentials_exception)

    # get the user from the database
    user = db.query(models.User).filter(models.User.id == token.user_id).first()