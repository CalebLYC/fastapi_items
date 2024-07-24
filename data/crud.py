import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def store_token(db: Session, user_id: int, token: str):
    db_token = models.Token(user_id=user_id, token=token)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def store_token_object(db: Session, token: schemas.Token):
    db_token = models.Token(**token.model_dump())
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_user_by_token(db: Session, token: str) -> models.User:
    db_token = db.query(models.Token).filter(models.Token.token == token).first()
    if not db_token:
        raise HTTPException(401, "Unauthorized")
    return db_token.user


def create_user(db: Session, user: schemas.UserCreate):
    # Hachage du mot de passe
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(
        email = user.email,
        username = user.username,
        fullname = user.fullname,
        hashed_password = hashed_password.decode('utf-8')
    )
    # Stockage dans la "base de données"
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item