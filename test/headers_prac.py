from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
app = FastAPI()

@app.get("/")
def root():
    return FileResponse("public_2/index.html")

@app.post("/postdata")
def postdata(username = Form(),userage = Form()):
    return {"name": username, "age": userage}
