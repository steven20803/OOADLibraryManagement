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

async def get_book_by_name(request: Request, book_name: str, db: Session = Depends(get_db)):
    stmt = select(Book).where(col(Book.book_name) == book_name)
    book = db.exec(stmt).one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return book

async def borrow_book(request: Request, book_id: int, user_id: int, db: Session = Depends(get_db)):
    # Find the book, user, max id of record
    stmt = select(Book).where(col(Book.id) == book_id)
    book = db.exec(stmt).one_or_none()
    stmt = select(User).where(col(User.id) == user_id)
    user = db.exec(stmt).one_or_none()
    stmt = select(func.max(Record.id))
    new_id = (db.exec(stmt).one_or_none() or 0) + 1

    # Check status
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            return
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            return
        )

    if book.status == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The book has been borrowed"
            return
        )

    if book.status == 2:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book lost"
            return
        )

    if book.status == 3:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book damaged"
            return
        )

    if book.status != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not available"
            return
        )

    # Modify database
    book.borrower_id = user.id
    book.last_borrowed = datetime.now()
    book.expected_return_time = datetime.now() + timedelta(weeks=1)
    book.status = 0

    # Create record
    record = Record(id=new_record_id, user_id=user.id, book_id=book.id, borrowed_time=datetime.now(), expected_return_time=book.expected_return_time)
    db.add(new_record)

    db.commit()
    db.refresh(book)
    return 'Book borrowed successfully'
