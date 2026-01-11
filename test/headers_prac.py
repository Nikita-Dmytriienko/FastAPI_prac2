from fastapi import FastAPI, Form
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def root():
    return FileResponse("public_2/index.html")

@app.post("/postdata")
def postdata(username: str = Form(),
             languages: list = Form()):
    return {"name": username, "languages": languages}