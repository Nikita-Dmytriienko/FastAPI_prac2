import uuid
from dataclasses import dataclass,field

from fastapi import FastAPI, Body, status, HTTPException
from fastapi.responses import JSONResponse, FileResponse

def generate_id():
    return str(uuid.uuid4())

@dataclass
class Person:
    name: str
    age: int
    id: str = field(default_factory=generate_id)



people = [Person("Tom", 38), Person("Bob", 42), Person("Sam", 28)]


def find_person(id):
    for person in people:
        if person.id is id:
            return person
    return None


app = FastAPI()


@app.get("/")
async def main():
    return FileResponse("public/index.html")


@app.get("/api/users")
def get_people():
    return people


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


@app.post("/api/users")
def create_person(data = Body()):
    person = Person(data["name"], data["age"])
    people.append(person)
    return person


@app.put("/api/users")
def edit_person(data = Body()):
    person = find_person(data["id"])
    if person is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not Found"}
        )
    person.age = data["age"]
    person.name = data["name"]
    return person


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
