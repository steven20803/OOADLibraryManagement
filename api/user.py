from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, col, select
from sqlalchemy import func, update

from dbHelper import get_db
from models.user import Role, User
from fastapi import HTTPException

router = APIRouter(tags=["user"], prefix="/user")


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
async def register_user(request: Request, username: str, set_password: str, db: Session = Depends(get_db)):
    try:
        stmt = select(User).where(col(User.name) == username)
        exists = db.exec(stmt).one_or_none()

        if exists is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists"
            )
        
        user = User(
            name=username,
            password=set_password,
            role=Role(1),
            status=True
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
async def login_user(request: Request, username: str, password: str, db: Session = Depends(get_db)):
    try:
        stmt = select(User).where(col(User.name) == username)
        exists = db.exec(stmt).one_or_none()

        if not exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists"
            )

        if exists.password != password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        return exists
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=User,
    response_model_exclude={"password"},
    summary="Get user by ID",
    responses={
        status.HTTP_200_OK: {"description": "User found"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def get_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=User,
    response_model_exclude={"password"},
    summary="Update user by ID",
    responses={
        status.HTTP_200_OK: {"description": "User updated successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Invalid data"},
    },
)
async def update_user(request: Request, user:User, db: Session = Depends(get_db)):
    stmt = select(User).where(col(User.id) == user.id)
    existing_user = db.exec(stmt).one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    stmt = (
        update(User).
        where(col(User.id) == user.id).
        values(
            name=user.name,
            password=user.password,
            role=Role(user.role),
            status=user.status
        )
    )
    try:
        db.exec(stmt)
        return existing_user
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid data"
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user by ID",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "User deleted successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db.delete(user)
    db.commit()
    return
