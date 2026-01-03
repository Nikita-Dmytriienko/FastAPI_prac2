from fastapi import FastAPI, Body
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def root():
    return FileResponse("../public/index.html")

@app.post("/hello")
def hello(name = Body(embed=True, min_length=3, max_length=50),
          age = Body(embed=True, ge= 18, lt=100)):
    # name = data ["name"]
    # age = data ["age"]
    return {"message": f"{name}, your age = {age} "}

