from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from requests import Session

from ..dependencies import get_db
from .auth import get_current_user
from ..data import crud, schemas

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Not authenticated"},
        403: {"description": "Forbidden"}
    },
)

@router.get("/me")
async def read_user_me(current_user: Annotated[schemas.User, Depends(get_current_user)]) -> schemas.User:
    return current_user


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)