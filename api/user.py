from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, col, select

from dbHelper import get_db
from models.user import Role, User

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
async def login_user(request: Request, db: Session = Depends(get_db)):
    stmt = select(User).where(col(User.name) == request.headers.get("username"))

    NotImplementedError("Implement the login logic here")
