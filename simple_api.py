import uuid
from dotenv import load_dotenv
import os

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse

from pydantic import BaseModel, Field

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from starlette.responses import JSONResponse


class UserSchema(BaseModel):
    name: str = Field(min_length=3, max_length=20,description="Name")
    age: int = Field(ge=18, lt=100, description="Age")

class UserResponse(BaseModel):
    id:str
    name:str
    age:int

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL dont found in .env file")

engine = create_engine(DATABASE_URL)

def find_person(id):
    for person in DATABASE_URL:
        if person.id == id:
            return person
    return None

app = FastAPI()

@app.get("/")
async def main():
    return FileResponse("public/index.html")


@app.get("/api/users/{id}")
def get_person(id):
    person = find_person(id)
    print(person)

    if person is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "user not found"}
        )

    return person


@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def create_person(user: UserSchema):
    new_user = UserResponse(
        id = str(uuid.uuid4()),
        name=user.name,
        age = user.age
    )
    DATABASE_URL.append(new_user)
    return new_user

@app.get("/api/users")
def get_people():
    return DATABASE_URL

@app.put("/api/users", status_code=status.HTTP_200_OK)
def edit_person(user_id: str, updated_data: UserSchema):
    for person in DATABASE_URL:
        if person.id == user_id:
            person.name = updated_data.name
            person.age = updated_data.age
            return person
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

@app.delete("/api/users/{id}", status_code=status.HTTP_200_OK)
def delete_person(id):
    person = find_person(id)
    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    DATABASE_URL.remove(person)
    return {"message": "User deleted"}
