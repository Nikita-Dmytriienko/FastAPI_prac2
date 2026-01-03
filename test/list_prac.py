from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int


app = FastAPI()


@app.get("/")
def root():
    return FileResponse("../public/index.html")

@app.post("/hello")
def hello(people: list[Person]):
    return {"message": people}