from fastapi import Depends, FastAPI

from .internal import admin
from .routers import items, users, auth
from .data import crud, models, schemas
from .data.database import engine

#create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(auth.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}