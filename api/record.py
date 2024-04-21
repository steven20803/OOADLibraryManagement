from typing import List

from fastapi import APIRouter, Depends, Request, status
from sqlmodel import Session, select

from dbHelper import get_db
from models.record import Record

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
