import mimetypes
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse, FileResponse
app = FastAPI()

@app.get("/")
def root():
    return FileResponse("index.html",
                        filename="mainpage.html",
                        media_type="application/octet-stream")
    
@app.get("/users/{id}")
def users(id):
    return {"user_id": id}
    