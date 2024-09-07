from src.repositories.auth import auth
from datetime import timedelta
from typing import Annotated
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
import configparser

# Models
from src.models.auth.user.create_user_request import CreateUserRequest
from src.models.responses.user_response import UserResponse
from src.models.auth.user.user import User
from src.models.auth.token.token import Token

# Environment variables
import configparser
config = configparser.ConfigParser()
config.read('.env')
ACCESS_TOKEN_EXPIRE_MINUTES = config['API']['ACCESS_TOKEN_EXPIRE_MINUTES']

# Repositories
from src.repositories.db.sql_alchemy_db import SessionLocal

# Instances
router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

# Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependencies
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth.get_current_user)]

# HTTP exceptions
unauthorized_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

# Router
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        username = create_user_request.username,
        hashed_password = auth.bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()
    return {
        "username": create_user_model.username,
        "id": create_user_model.id
    }

@router.post('/token', status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    token = auth.create_access_token(user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {
        'access_token': token,
        'token_type': 'bearer'
    }

@router.get("/user", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise unauthorized_exception
    return user