from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, col, select
from sqlalchemy import func, update

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

@router.post(
    "/book_create",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
    summary="Create a new book",
    responses={
        status.HTTP_201_CREATED: {"description": "Book created successfully"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Invalid data"},
    },
)
async def create_book(request: Request, title: str, authors: str, db: Session = Depends(get_db)):
    try:
        book = Book(
            book_name=title,
            author=authors,
            borrowed=False,
            borrower_id=None,
            last_borrowed=None,
            status=True,
            comments=""
        )
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid data"
        )
    
@router.put(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=Book,
    summary="Update a book by id",
    responses={
        status.HTTP_200_OK: {"description": "Book updated"},
        status.HTTP_404_NOT_FOUND: {"description": "Book not found"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Invalid data"},
    },
)
async def update_book(request: Request, book: Book, db: Session = Depends(get_db)):
    stmt = select(Book).where(col(Book.id) == book.id)
    existing_book = db.exec(stmt).one_or_none()

    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    stmt = (
        update(Book).
        where(col(Book.id) == book.id).
        values(
            book_name=book.book_name,
            author=book.author,
            borrowed=book.borrowed,
            borrower_id=book.borrower_id,
            last_borrowed=book.last_borrowed,
            status=book.status,
            comments=book.comments
        )
    )
    try:
        db.exec(stmt)
        return existing_book
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid data"
        )
    
@router.delete(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a book by id",
    responses={
        status.HTTP_200_OK: {"description": "Book deleted"},
        status.HTTP_404_NOT_FOUND: {"description": "Book not found"},
    },
)
async def delete_book_by_id(request: Request, book_id: int, db: Session = Depends(get_db)):
    stmt = select(Book).where(col(Book.id) == book_id)
    book = db.exec(stmt).one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    db.delete(book)
    db.commit()
    return book