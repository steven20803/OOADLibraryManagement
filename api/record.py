from typing import List

from fastapi import APIRouter, Depends, Request, status, HTTPException
from sqlmodel import Session, select
from models.book import Book
from models.user import User

from dbHelper import get_db
from models.record import Record
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime, timedelta

router = APIRouter(tags=["record"], prefix="/record")


@router.get(
    "/Records",
    status_code=status.HTTP_200_OK,
    response_model=List[Record],
    summary="Get all records by paging, default page=1, per_page=10",
    responses={
        status.HTTP_200_OK: {"description": "Records retrieved successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "No records found"},
    },
)
async def read_records(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 10,
):
    skip = (page - 1) * per_page
    records = db.exec(select(Record).offset(skip).limit(per_page)).all()
    return records
    
@router.get("/search_record")
async def search_record(book_name: str, db: Session = Depends(get_db)):
#  try:  
    # 查詢 Book 表，獲取 Book 的 id
    from models.book import Book
    book = db.exec(select(Book).where(Book.book_name == book_name)).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="No book found with the given name.")
    
    # 使用 Book 的 id 查詢 Record 表
    # record = Record.get_record_by_book_id(db, book.id)
    
    from models.record import Record
    record = db.exec(select(Record).where(Record.book_id == book.id)).first()
    if record:
        # 呈現 Record 資訊
        return {
            'id': record.id,
            'user_id': record.user_id,
            'book_id': record.book_id,
            'borrowed_time': record.borrowed_time,
            'expected_return_time': record.expected_return_time,
            'actual_return_time': record.actual_return_time
            #'returned': record.returned
        }
    else:
        raise HTTPException(status_code=404, detail="No record found for the book.")
        
async def create_record_by_id(
    request: Request,
    user_id: int,
    book_id: int,
    db: Session = Depends(get_db)
):
    stmt = select(Book).where(col(Book.id) == book_id)
    book = db.exec(stmt).one_or_none()
    stmt = select(User).where(col(User.id) == user_id)
    user = db.exec(stmt).one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    
    record = Record(
        user_id=user_id,
        book_id=book_id,
        borrowed_time = datetime.now(),
        expected_return_time = datetime.now() + timedelta(days=7),
        astual_return_time = None
    )

    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid data"
        )


@router.put(
    "/{record_id}",
    status_code=status.HTTP_200_OK,
    response_model=Record,
    summary="Update a record by ID",
    responses={
        status.HTTP_200_OK: {"description": "Record updated successfully"},
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid record data"},
        status.HTTP_404_NOT_FOUND: {"description": "Record not found"},
    },
)
async def update_record(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
):
    stmt = select(Record).where(col(Record.id) == id)
    existing_record = db.exec(stmt).one_or_none()

    if not existing_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )
    stmt = (
        update(Record).
        where(col(Record.id) == id).
        values(
            actual_return_time = datetime.now(),
        )
    )
    try:
        db.exec(stmt)
        return existing_record
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid data"
        )


@router.delete(
    "/{record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a record by ID",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Record deleted successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "Record not found"},
    },
)
async def delete_record_by_id(request: Request, record_id: int, db: Session = Depends(get_db)):
    stmt = select(Record).where(col(Record.id) == record_id)
    record = db.exec(stmt).one_or_none()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    db.delete(record)
    db.commit()
    return record
