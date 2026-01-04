import uuid
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import FileResponse

from pydantic import BaseModel, Field

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, Mapped, mapped_column

from dotenv import load_dotenv
import os

#load .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL dont found in .env file")

engine = create_async_engine(DATABASE_URL, pool_size=20, max_overflow=10)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # name = Column(String(20), nullable=False)
    # age = Column(Integer, nullable=False)
    # Base.metadata.create_all(bind=engine)

    #new style for sqlalchemy 2.0
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=20,description="Name")
    age: int = Field(ge=18, lt=100, description="Age")

class UserResponse(BaseModel):
    id: uuid.UUID
    name:str
    age:int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=20)
    age: int | None = Field(None, ge=18, lt=100)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
async def main():
    return FileResponse("public/index.html")

#GET all users
@app.get("/api/users/")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()

#GET user from id
@app.get("/api/users/{user_id}")
def get_person(user_id: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


#CREATE
@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def create_person(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = UserDB(
        name=user_data.name,
        age = user_data.age
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # id from db
    return new_user

#UPDATE
@app.put("/api/users", status_code=status.HTTP_200_OK)
def update_person(
        user_id: str,
        user_data: UserUpdate,
        db: Session = Depends(get_db)
):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user_data.name
    user.age = user_data.age
    db.commit()
    db.refresh(user)
    return user

#DELETE
@app.delete("/api/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_person(user_id: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
