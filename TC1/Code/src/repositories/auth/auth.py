# Imports
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import HTTPException, Depends
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Models
from src.models.auth.user.user import User

# Instances
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# Environment variables
import configparser
config = configparser.ConfigParser()
config.read('.env')
SECRET_KEY = config['API']['SECRET_KEY']
ALGORITHM = config['API']['ALGORITHM']

# HTTP exceptions
unauthorized_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

# Internal functions
def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    global unauthorized_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise unauthorized_exception
        return {
            'username': username,
            'id': user_id
        }
    except JWTError:
        raise unauthorized_exception
