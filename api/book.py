from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, col, select
from sqlalchemy import func, update

from dbHelper import get_db
from models.book import Book
from models.user import User
from models.record import Record

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

@router.get(
    "/{book_name}",
    status_code=status.HTTP_200_OK,
    response_model=Book,
    summary="Get a book by name",
    responses={
        status.HTTP_200_OK: {"description": "Book retrieved"},
        status.HTTP_404_NOT_FOUND: {"description": "Book not found"},
    },
)
async def get_book_by_name(request: Request, book_name: str, db: Session = Depends(get_db)):
    stmt = select(Book).where(col(Book.book_name) == book_name)
    book = db.exec(stmt).one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return book

@router.put(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=Book,
    summary="Borror a book by id",
    responses={
        status.HTTP_200_OK: {"description": "Book borrowed successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "Book not found"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Invalid data"},
    },
)
async def borrow_book(request: Request, book_id: int, user: User, db: Session = Depends(get_db)):
    # Find the book, user, max id of record
    stmt = select(Book).where(col(Book.id) == book_id)
    book = db.exec(stmt).one_or_none()
    stmt = select(func.max(Record.id))
    new_id = (db.exec(stmt).one_or_none() or 0) + 1

    # Check status
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if book.status == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The book has been borrowed"
        )

    if book.status == 2:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book lost"
        )

    if book.status == 3:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book damaged"
        )

    if book.status != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not available"
        )

    # Modify database
    book.borrower_id = user.id
    book.last_borrowed = datetime.now()
    book.expected_return_time = datetime.now() + timedelta(weeks=1)
    book.status = 0

    # Create record
    record = Record(id=new_id, user_id=user.id, book_id=book.id, borrowed_time=datetime.now(), expected_return_time=book.expected_return_time)
    db.add(record)

    db.commit()
    db.refresh(record)
    return 'Book borrowed successfully'
  
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

@router.put(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=Book,
    summary="Return a book by id",
    responses={
        status.HTTP_200_OK: {"description": "Book returned successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "Book not found"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Invalid data"},
    },
)
async def return_book(request: Request, book_id: int, record: Record, db: Session = Depends(get_db)):
    # Find the book, user, max id of record
    stmt = select(Book).where(col(Book.id) == book_id)
    book = db.exec(stmt).one_or_none()

    # Check status
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    
    if book.status == 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not available"
        )

    if book.status == 2:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book lost"
        )

    if book.status == 3:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book damaged"
        )
    
    if book.status != 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The book is not borrowed"
        )
    
    if book.id != record.book_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The book is not the one in the record"
        )
    
    # Modify database
    book.status = 1

    # Modify record
    record.actual_return_time = datetime.now()
    db.refresh(record)
    return 'Book returned successfully'
