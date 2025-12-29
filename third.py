import mimetypes
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, PlainTextResponse

app = FastAPI()

@app.get("/old")
def old():
    return RedirectResponse("/new")

@app.get("/new")
def new():
    return PlainTextResponse("New Page")