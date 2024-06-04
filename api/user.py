from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, col, select

from dbHelper import get_db
from models.user import Role, User


import bcrypt
import jwt
from passlib.context import CryptContext


router = APIRouter(tags=["user"], prefix="/user")

# 初始化密碼上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 密鑰和算法（確保這是秘密的並存放在環境變數中）
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
    response_model_exclude={"password"},
    summary="Register a new user",
    responses={
        status.HTTP_201_CREATED: {"description": "User created successfully"},
        status.HTTP_409_CONFLICT: {"description": "User already exists"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Invalid data"},
    },
)
async def register_user(request: Request, user: User, db: Session = Depends(get_db)):
    try:
        user.role = Role(user.role)
        stmt = select(User).where(col(User.name) == user.name)
        exists = db.exec(stmt).one_or_none()

        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists"
            )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid data"
        )


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Login user",
    responses={
        status.HTTP_200_OK: {"description": "User logged in successfully"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials"},
    },
)
async def login_user(request: Request, user: User, db: Session = Depends(get_db)):
    '''
        stmt = select(User).where(col(User.name) == request.headers.get("username"))

        NotImplementedError("Implement the login logic here")
    '''
    user_data = await request.json()
    username = user_data.get("username")
    password = user_data.get("password")
    
    if not ( username ) or ( not password ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login Invalid credentials")


    stmt = select(User).where(col(User.name) == username) 
    result = db.exec(stmt).one_or_none()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials--user not found"
        )
    
    user = result.scalar().first

    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials--wrong password")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.name}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    responses={
        status.HTTP_200_OK:{"description": "User logged out successfully"},
        status.HTTP_401_UNAUTHORIZED:{"description": "Unauthorized access"},
    },
)
async def logout_user(request: Request, db: Session = Depends(get_db)): 
    # Get the user's token from the request
    token = request.headers.get("Authorization")

    # Check if the token is valid
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")

    # Invalidate the token
    # For example, you can delete the token from the database
    stmt = select(User).where(col(User.token) == token)
    result = db.exec(stmt).one_or_none()
    user = result.scalar().first
    if user:
        user.token = None
        db.commit()

    return {"message": "User logged out successfully"}

