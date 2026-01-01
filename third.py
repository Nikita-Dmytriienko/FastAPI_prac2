from fastapi import FastAPI, Body
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def root():
    return FileResponse("public/index.html")

@app.post("/hello")
def hello(name = Body(embed=True), age = Body(embed=True)):
    # name = data ["name"]
    # age = data ["age"]
    return {"message": f"{name}, your age = {age} "}

