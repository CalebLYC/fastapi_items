import datetime
from typing import Annotated, Union
import bcrypt
from fastapi import APIRouter, Header, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from requests import Session

from ..dependencies import get_db

from ..data import crud
from ..data import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    tags=["Auth"],
    dependencies=[],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Not authenticated"},
        403: {"description": "Forbidden"}
    },
)

# Clé secrète pour signer les tokens
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    user = crud.get_user_by_token(token=token, db=db)
    return user


@router.post("/login", response_model=schemas.User)
async def login(user: schemas.UserAuth, db: Session = Depends(get_db), ):
    db_user = crud.get_user_by_email(email=user.email, db=db)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    token = schemas.TokenCreate(token=access_token, user_id=db_user.id)
    crud.store_token_object(db, token=token)
    crud.get_user_by_email(email=user.email, db=db)
    return db_user


@router.post("/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)