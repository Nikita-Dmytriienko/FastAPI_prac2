from typing import Optional
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str
    age: Optional[int] = None
    
app = FastAPI()

@app.get("/")
def root():
    return FileResponse("public/index.html")


@app.post("/hello")
def hello(person: Person):
    if person.age == None:
        return {"message": f"Hi, {person.name}"}
    else:
        return {"message": f"Hi, {person.name}, your age is {person.age}"}