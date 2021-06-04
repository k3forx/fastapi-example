from datetime import datetime, timedelta
from logging import getLogger
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from mysql_client import mysql
from passlib.context import CryptContext

from .models import Token, TokenData, User, UserBeforeRegister, UserInDB

router = APIRouter()
logger = getLogger(__name__)

SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    logger.info("Verify password")
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    query = f"SELECT * FROM users WHERE username = '{username}';"
    user_info = mysql.execute_fetch_query(query)[0]
    if not user_info:
        return
    else:
        logger.info("The user is found")
        user_dict = {
            "id": user_info[0],
            "username": user_info[1],
            "hashed_password": user_info[2],
            "disabled": user_info[3],
            "created_at": user_info[4],
        }  # TODO: Use ORM
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        logger.info("password is wrong")
        return False
    logger.info("authentication is finished")
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info("Authenticate a user")
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info(f"Authenticated: login user is {user.username}")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register_new_user(register_user: UserBeforeRegister):
    logger.info(f"Register a new user. username: {register_user.username}")
    hashed_password = get_password_hash(register_user.raw_password)
    query = f"INSERT INTO users (username, password) VALUES ('{register_user.username}', '{hashed_password}');"
    try:
        mysql.execute_commit_query(query)
        logger.info("The user is registered successfully")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "The user is successfully created"})
    except Exception as e:
        logger.error(f"Failed to register a new user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register a new user",
        )
