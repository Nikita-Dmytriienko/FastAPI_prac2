import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, status, Path, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response

from pydantic import BaseModel, ConfigDict, Field

from sqlalchemy import String, Integer, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")


async_engine = create_async_engine(DATABASE_URL, pool_size=20, max_overflow=10)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    
app = FastAPI(lifespan=lifespan)

app.mount("/",
           StaticFiles(
               directory="public",
               html=True),
               name="static")
    
class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=20, description="Name")
    age: int = Field(ge=18, lt=100, description="Age")


class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    age: int

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=20)
    age: int | None = Field(None, ge=18, lt=100)


# GET ALL USERS
@app.get("/api/users/",response_model=list[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Limit for pagination")
):
    query = select(UserDB).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


# GET BY ID USER
@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_person(
        user_id: uuid.UUID = Path(
            ...,
            description="User UUID",
            examples={"example": {"value": "550e8400-e29b-41d4-a716-446655440032"}}
        ),
        db: AsyncSession = Depends(get_db)
):
    user = await db.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# CREATE USER
@app.post("/api/users/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_person(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = UserDB(name=user_data.name, age=user_data.age)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# UPDATE USER
@app.put("/api/users/{user_id}", response_model=UserResponse)
async def update_person(
        user_data: UserUpdate,
        user_id: uuid.UUID = Path(..., description="User UUID"),
        db: AsyncSession = Depends(get_db)
):
    user = await db.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_data.name is not None:
        user.name = user_data.name
    if user_data.age is not None:
        user.age = user_data.age

    await db.commit()
    await db.refresh(user)
    return user


# DELETE USER
@app.delete("/api/users/{user_id}")
async def delete_person(
        user_id: uuid.UUID = Path(..., description="User UUID"),
        db: AsyncSession = Depends(get_db)
):
    user = await db.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"detail": "User deleted"}
