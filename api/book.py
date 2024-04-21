from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, col, select

from dbHelper import get_db
from models.book import Book

router = APIRouter(tags=["book"], prefix="/book")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[Book],
    summary="Get all books by paging, default page=1, per_page=10",
    responses={
        status.HTTP_200_OK: {"description": "Books retrieved successfully"},
    },
)
async def get_all_books(
    request: Request, db: Session = Depends(get_db), page: int = 1, per_page: int = 10
):
    skip = (page - 1) * per_page
    stmt = select(Book).offset(skip).limit(per_page)
    return db.exec(stmt).all()


@router.get(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=Book,
    summary="Get a book by id",
    responses={
        status.HTTP_200_OK: {"description": "Book retrieved"},
        status.HTTP_404_NOT_FOUND: {"description": "Book not found"},
    },
)
async def get_book_by_id(request: Request, book_id: int, db: Session = Depends(get_db)):
    stmt = select(Book).where(col(Book.id) == book_id)
    book = db.exec(stmt).one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return book
