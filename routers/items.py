from fastapi import APIRouter, Depends, HTTPException
from requests import Session

from ..data import crud, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Not authenticated"},
        403: {"description": "Forbidden"}
    },
)

@router.get("/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items