from typing import List

from fastapi import APIRouter, Depends, Request, status, HTTPException
from sqlmodel import Session, select

from dbHelper import get_db
from models.record import Record
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(tags=["record"], prefix="/record")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[Record],
    summary="Get all records by paging, default page=1, per_page=10",
    responses={
        status.HTTP_200_OK: {"description": "Records retrieved successfully"},
        status.HTTP_404_NOT_FOUND: {"description": "No records found"},
    },
)
def read_records(
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
