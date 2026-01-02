import uuid

from fastapi import FastAPI, Body, status, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    name: str = Field(min_length=3, max_length=20,description="Name")
    age: int = Field(default=18, ge=18, lt=100, description="Age")

class UserResponse(BaseModel):
    id:str

people =[]

def find_person(id):
    for person in people:
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
    people.append(new_user)
    return new_user

@app.get("/api/users")
def get_people():
    return people

@app.put("/api/users", status_code=status.HTTP_202_ACCEPTED)
def edit_person(user_id: str, updated_data: UserSchema):
    for person in people:
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
    people.remove(person)
    return {"message": "User deleted"}
